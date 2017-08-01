from copy import copy

from hyperopt import hp

#################################################################
# Dictionary for: step_detection_single_side
#################################################################
d = dict()

# Side to work on
d['side'] = 'lhs'

# Signal to use
d['signal_to_use'] = 'norm'
d['do_windows_if_vertical'] = False
d['vert_win'] = 1

# choose which smoothing to perform (or none at all if mva_win is equal to ~1
d['smoothing'] = 'mva'
d['mva_win'] = 5 + hp.randint('mva_win', 50)
d['butter_freq'] = 1

# Peak detection algorithm and parameters
d['peak_type'] = 'peak_utils'
d['p1_sc'] = 1
d['p2_sc'] = 2
d['p1_pu'] = hp.uniform('p1_pu', 0.1, 1)
d['p2_pu'] = 5 + 5 * hp.randint('p2_pu', 9)

# Choose whether to remove weak signals
d['remove_weak_signals'] = False
# d['weak_signal_thresh'] = hp.uniform('weak_signal_thresh', -1, 0.5)
d['weak_signal_thresh'] = 1

# Save
space_single_side_lhs = d
space_single_side_lhs['side'] = 'lhs'

space_single_side_rhs = copy(d)
space_single_side_rhs['side'] = 'rhs'

#################################################################
# Dictionary for: step_detection_two_sides_overlap
#################################################################
d = dict()

# Signal to use
d['signal_to_use'] = 'norm'
d['do_windows_if_vertical'] = False
d['vert_win'] = 5

# choose which smoothing to perform (or none at all if mva_win is equal to ~1
d['smoothing'] = 'mva'
d['mva_win'] = 5 + hp.randint('mva_win', 50)
d['butter_freq'] = 1

# Peak detection algorithm and parameters
d['peak_type'] = 'peak_utils'
d['p1_sc'] = 1
d['p2_sc'] = 2
d['p1_pu'] = hp.uniform('p1_pu', 0.1, 1)
d['p2_pu'] = 5 + 5 * hp.randint('p2_pu', 9)

# Signal merging parameters
d['win_size_merge'] = 2 + 2 * hp.randint('win_size_merge', 20)
d['win_size_remove_adjacent_peaks'] = 2 + 2 * hp.randint('win_size_remove_adjacent_peaks', 15)

# Save
space_overlap = d

#################################################################
# Dictionary for: step_detection_two_sides_combined_signal
#################################################################
d = dict()

# Signal to use
d['signal_to_use'] = 'norm'
d['do_windows_if_vertical'] = False
d['vert_win'] = 5

# Smoothing to perform on signals before combining(or none at all if mva_win is equal to ~1)
d['smoothing'] = 'mva'
d['mva_win'] = 5 + hp.randint('mva_win', 50)
d['butter_freq'] = 1

# Smoothing after combining signals
d['mva_win_combined'] = 5 + 2 * hp.randint('mva_win_combined', 25)

# Choosing the more sine-like combined signal
d['min_hz'] = hp.uniform('min_hz', 0.1, 2)
d['max_hz'] = d['min_hz'] + 0.1 + hp.uniform('max_hz', 0.1, 3)
d['factor'] = 0.5 + 0.1 * hp.randint('butter_freq', 10)


# Peak detection algorithm and parameters
d['peak_type'] = 'peak_utils'
d['p1_sc'] = 1
d['p2_sc'] = 2
d['p1_pu'] = hp.uniform('p1_pu', 0.1, 1)
d['p2_pu'] = 5 + 5 * hp.randint('p2_pu', 9)

# Save
space_combined = d
