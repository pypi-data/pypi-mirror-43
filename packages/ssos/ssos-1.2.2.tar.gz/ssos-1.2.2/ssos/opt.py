'''
    Extraction of cutouts of SSOs using SWarp,
    cross-matching with the SkyBoT database, and other analyses.

    Part of the SSO recovery pipeline.
'''

import os
import urllib.request

from astropy.io import fits
from astropy.io.votable import parse_single_table
from astropy.time import Time
import numpy as np
import pandas as pd


def extract_cutouts(sources, settings, log, paths, args):
    '''
        Extract cutouts of sources found in SCAMP catalogues using SWARP

        input
        ------
        sources - pd.DataFrame, table of source data
        settings - dict, dictionary of pipeline settings with PARAM:VALUE pairs
        log - logging object
        paths - dict, absolute paths of target directories
        args - command line argument parser

        return
        ------
        sources - pd.DataFrame, table of source data (unchanged)
    '''

    log.info('\nExtracting cutouts with SWARP..')

    image_dir    = args.fields[0]
    cutout_dir   = paths['cutouts']
    cutout_size  = settings['CUTOUT_SIZE']
    swarp_config = settings['SWARP_CONFIG']

    for index, row in sources.iterrows():

        image_file = os.path.join(image_dir, row['IMAGE_FILENAME']) + '[%i]' % row['EXTENSION']

        cutout_filename = os.path.join(cutout_dir, '{:.0f}_{:.0f}.fits'.format(row['SOURCE_NUMBER'],
                                                                               row['CATALOG_NUMBER']))

        if not args.swarp and os.path.isfile(cutout_filename):
            log.debug('Cutout %s exists, skipping..' % cutout_filename)
            continue

        swarp_args = {
                    'file': image_file,
                    'config': swarp_config,
                    'overwrite_params': {
                        'WEIGHTOUT_NAME': os.path.join(paths['tmp'], 'tmp_weight'),
                        'CENTER'        : '{:.5f},{:.5f}'.format(row['ALPHA_J2000'], row['DELTA_J2000']),
                        'IMAGEOUT_NAME' : '{:s}'.format(cutout_filename),
                        'IMAGE_SIZE'    : str(cutout_size),
                        'COPY_KEYWORDS' : 'OBJECT,RA,DEC,FILTER,DATE-OBS'},
                    }
        # ------
        # Build command and execute SWARP
        cmd = ' '.join(['swarp', swarp_args['file'], '-c', swarp_args['config']])
        for param, value in swarp_args['overwrite_params'].items():
            cmd += ' '.join([' -' + param, value])

        log.debug('\nExecuting SWARP command:\n%s' % cmd)
        if log.level > 10:  # Shown SWARP warnings only when debugging
            cmd += ' >/dev/null 2>&1'
        os.system(cmd)

    log.info('\tDone.\n')
    return sources


def compute_aperture_magnitudes(sources, settings, log, paths, args):
    '''
    Executes SExtractor in dual image mode and computes fixed aperture magnitudes

    input
    ------
    sources - pd.DataFrame, table of source data
    settings - dict, dictionary of pipeline settings with PARAM:VALUE pairs
    log - logging object
    paths - dict, absolute paths of target directories
    args - command line argument parser

    return
    ------
    sources - pd.DataFrame, table of source data with new magnitudes
    '''

    log.info('Computing fixed aperture magnitudes with SExtractor..')

    cutout_dir = paths['cutouts']
    cutouts = [os.path.join(cutout_dir, cutout) for cutout in os.listdir(cutout_dir)
               if cutout.endswith('.fits')]
    reference_filter = settings['REFERENCE_FILTER'].split(',')

    for number, source in sources.groupby('SOURCE_NUMBER'):

        # Select detection image based on reference filter
        filter_found = False
        for filter_ in reference_filter:
            try:
                reference_detection = source.loc[source['FILTER'] == filter_].iloc[0]
                filter_found = True
            except IndexError:
                continue
            if filter_found:
                sources.loc[(sources.SOURCE_NUMBER == reference_detection.SOURCE_NUMBER) &
                            (sources.CATALOG_NUMBER == reference_detection.CATALOG_NUMBER), 'FLAGS_SSOS'] += 2
                break
        else:
            from ssos.core import PipelineSettingsException
            raise PipelineSettingsException('No detection of candidate %i found in reference filter %s.'\
                                            % (number, reference_filter))

        detection_image = os.path.join(cutout_dir, '_'.join([str(number),
                                                             str(reference_detection['CATALOG_NUMBER'])])
                                                             + '.fits')

        # ------
        # Call SExtractor in dual image mode
        for image in cutouts:

            if str(number) not in image:
                continue

            cat = os.path.join(paths['cutouts'], os.path.basename(image.replace('.fits', '.cat')))

            if image == detection_image:
                detection_cat = cat

            sex_args = {
                'file': ','.join([detection_image, image]),
                'config': settings['SEX_CONFIG'],
                'overwrite_params': {
                    'PARAMETERS_NAME': settings['SEX_PARAMS'],
                    'CATALOG_NAME'   : cat,
                    'WEIGHT_TYPE'    : 'BACKGROUND',
                    'FILTER_NAME'    : settings['SEX_FILTER'],
                    'STARNNW_NAME'   : settings['SEX_NNW'],
                },
            }

            # ------
            # Exectue SExtractor
            cmd = ' '.join(['sex', sex_args['file'], '-c', sex_args['config']])
            for param, value in sex_args['overwrite_params'].items():
                cmd += ' '.join([' -' + param, value])
            os.system(cmd)

        # Identify the SSO in the detection cat to track it among the other ones
        cutout_size = settings['CUTOUT_SIZE']

        with fits.open(detection_cat) as detection_cat:

            # ------
            # Find the source closes to the center coordinate
            x_images = detection_cat[2].data.field('XWIN_IMAGE')
            y_images = detection_cat[2].data.field('YWIN_IMAGE')

            # Get 2d distances of sources to image center
            distances = [np.linalg.norm(np.array([cutout_size, cutout_size]) / 2 - np.array([x_img, y_img]))
                         for x_img, y_img in zip(x_images, y_images)]

            # Find index of source closest to center -> SSO candidate
            center_source_ind = np.where(distances == np.min(distances))[0]

        for ind, detection in source.iterrows():

            catalog = os.path.join(cutout_dir, '_'.join([str(detection.SOURCE_NUMBER),
                                                         str(detection.CATALOG_NUMBER)]) + '.cat')

            with fits.open(catalog) as cat:
                for prop in ['MAG', 'FLUX']:
                    sources.loc[ind, prop + '_CI'] = cat[2].data.field(prop + '_AUTO')[center_source_ind]
                    sources.loc[ind, prop + 'ERR_CI'] = cat[2].data.field(prop + 'ERR_AUTO')[center_source_ind]

    log.info('\tDone.\n')

    return sources


def _query_and_cross_match(group, target_dir, fov, obs_code, crossmatch_radius, log, args):
    '''
    Retrieves the SkyBoT query XML file for sources grouped by the DATE-OBS keyword

    input
    ------
    group - pd.DataFrame, table of source data
    target_dir - str, absolute path to SkyBoT folder
    fov - str, value of FOV_DIMENSIONS parameter
    obs_code - str, value of OBSERVATORY_CODE parameter
    crossmatch_radius - float, crossmatch radius in degree
    log - logging object
    args - command line argument parser

    return
    -------
    group - pd.DataFrame group, sources grouped by DATE-OBS with SkyBoT data added
    '''

    # ------
    # Download SkyBoT query results to VOTABLE

    # Get mid-exposure epoch
    epoch = group['MID_EXPOSURE_MJD'].tolist()[0]
    epoch = Time(epoch, format='mjd')
    mid_exposure = epoch.isot

    ra_field = group['RA_IMAGE'].tolist()[0]
    dec_field = group['DEC_IMAGE'].tolist()[0]

    query_url = 'http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?-ep=%s&-ra=%s&-dec=%s'\
                '&-bd=%s&-mime=votable&-output=basic&-loc=%s&-filter=0&-objFilter=111&&-from=AF&-top=' %\
                (mid_exposure, ra_field, dec_field, fov, obs_code)

    output_filename = 'skybot_%s_%s_%s.xml' % (ra_field, dec_field, mid_exposure)
    output_filename = os.path.join(target_dir, output_filename)

    if not args.skybot and os.path.isfile(output_filename):
            log.debug('\nAlready queried %s, skipping download..' % output_filename)
    else:
        try:
            urllib.request.urlretrieve(query_url, output_filename)
        except urllib.error.URLError as err:
            log.info('SkyBoT query failed: {0}'.format(err))

    # ------
    # Cross-match query results with sources from that epoch
    try:
        # Temporarily disable warnings as otherwise astropy.io.votable.tree
        # will spam the output with xml warnings
        import warnings
        warnings.filterwarnings('ignore')
        skybot_sources = parse_single_table(output_filename).array
        warnings.filterwarnings('default')
        skybot_sources = pd.DataFrame(np.ma.filled(skybot_sources))

    except (IndexError, FileNotFoundError):
        # No matches in SkyBoT database were found or error in query
        skybot_sources = pd.DataFrame({'number': [''],
                                       'name': [''],
                                       'magV': [0],
                                       '_raj2000': [0],
                                       '_decj2000': [0],
                                       'dracosdec': [0],
                                       'ddec': [0],
                                       'class': ['']})

    # Call actual cross-matching method on single source detections
    group = group.apply(_cross_match, args=(skybot_sources, crossmatch_radius), axis=1)

    return group


def _cross_match(source, skybot_sources, crossmatch_radius):
    '''
        Cross-matching is applied to single rows in database.  Checks for matches
        and adds SkyBoT source parameters to database if a match is found.

        input
        ------
        source - pd.Series, single source detection parameters
        skybot_sources - pd.DataFrame, parameters of all SkyBoT sources in exposure
        crossmatch_radius - float, crossmatch radius in arcsec

        returns
        source - pd.Series, single source detection parameters with SkyBot parameters added
    '''

    # Find SkyBoT source that is closest in angular separation to source
    distances_to_source = abs(np.sqrt((skybot_sources['_raj2000'] - source['ALPHA_J2000'])**2 +\
                                      (skybot_sources['_decj2000'] - source['DELTA_J2000'])**2))

    if distances_to_source.min() <= crossmatch_radius:

        skybot_match = skybot_sources.iloc[distances_to_source.values.argmin()]

        source['SKYBOT_NUMBER']  = skybot_match['num']
        source['SKYBOT_NAME']    = skybot_match['name']
        source['SKYBOT_MAG']     = skybot_match['magV']
        source['SKYBOT_ALPHA']   = skybot_match['_raj2000']
        source['SKYBOT_DELTA']   = skybot_match['_decj2000']
        source['SKYBOT_PMALPHA'] = skybot_match['dracosdec']
        source['SKYBOT_PMDELTA'] = skybot_match['ddec']
        source['SKYBOT_CLASS']   = skybot_match['class']

    return source


def _compute_pm_difference_angle(row):
    # returns the angle between the skybot and source proper motion vectors
    skybot_pm = np.array([row.SKYBOT_PMALPHA, row.SKYBOT_PMDELTA])

    try:
        skybot_pm /= np.linalg.norm(skybot_pm)

    except ValueError: # no skybot match
        return 100.    # should never be the largest angle

    source_pm = np.array([row.PMALPHA_J2000, row.PMDELTA_J2000])
    source_pm /= np.linalg.norm(source_pm)

    return np.arccos(np.clip(np.dot(source_pm, skybot_pm), -1.0, 1.0))


def crossmatch_skybot(sources, settings, log, paths, args):
    '''
    Query SkyBoT for each epoch and cross-match the expected SSOs
    with the sources in the database.  Requires working internet connection.

    input
    ------
    sources - pd.DataFrame, table of source data
    settings - dict, dictionary of pipeline settings with PARAM:VALUE pairs
    log - logging object
    paths - dict, absolute paths of target directories
    args - command line argument parser

    return
    ------
    sources - pd.DataFrame, table of source data with SkyBoT matches added
    '''
    log.info('\nCross-matching SSO candidates with SkyBoT..')


    target_dir = paths['skybot']
    fov        = settings['FOV_DIMENSIONS']
    obs_code   = settings['OBSERVATORY_CODE']
    crossmatch_radius = settings['CROSSMATCH_RADIUS'] / 3600 # convert from arcsecond to degrees


    # The default value for the SkyBoT columns are empty strings
    sources = pd.concat([sources, pd.DataFrame('', sources.index,
                        ['SKYBOT_NAME', 'SKYBOT_NUMBER', 'SKYBOT_CLASS', 'SKYBOT_MAG',
                         'SKYBOT_ALPHA', 'SKYBOT_DELTA', 'SKYBOT_PMALPHA', 'SKYBOT_PMDELTA'])], axis=1)

    # Cross-match for each mid-exposure epoch
    sources = sources.groupby('DATE-OBS').apply(_query_and_cross_match, target_dir=target_dir,
                                                    fov=fov, obs_code=obs_code, log=log, args=args,
                                                    crossmatch_radius=crossmatch_radius)

    # For each SSO, check if multiple matches were found
    # If so, choose the match which is most co-linear with the measured proper motion (minimize the angles)
    for number, source in sources.groupby('SOURCE_NUMBER'):

        if len(set(source.SKYBOT_NAME)) > 1:
            # if one of the matches is NaN, remove it and see if there's only one left
            names = set([name for name in source.SKYBOT_NAME if name != ''])

            if len(names) == 1: # some detections were not matched, add the designation to their columns

                numbers = [numb for numb in source.SKYBOT_NUMBER if numb != '']
                sources.loc[source.index, 'SKYBOT_NAME'] = list(names)[0]
                sources.loc[source.index, 'SKYBOT_NUMBER'] = list(numbers)[0]

            else: # compute the best match by minimizing the angular difference in proper motion

                pm_difference = source.apply(_compute_pm_difference_angle, axis=1)
                best_match = pm_difference.idxmin()

                best_match_name = sources.loc[best_match, 'SKYBOT_NAME']
                best_match_number = sources.loc[best_match, 'SKYBOT_NUMBER']

                sources.loc[source[source.SKYBOT_NAME != best_match_name].index,
                                  ['SKYBOT_NAME', 'SKYBOT_NUMBER', 'SKYBOT_MAG',
                                   'SKYBOT_ALPHA', 'SKYBOT_DELTA', 'SKYBOT_PMALPHA',
                                   'SKYBOT_PMDELTA', 'SKYBOT_CLASS']] = [best_match_name, best_match_number,
                                                                         '', '', '', '', '', '']

    log.info(' %i matched.\n' % len(set(sources[sources['SKYBOT_NAME']!='']['SOURCE_NUMBER'])))
    return sources