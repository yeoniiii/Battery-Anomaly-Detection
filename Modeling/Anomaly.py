import pandas as pd
import numpy as np
from scipy import stats
import math

class Anomaly(object):
    def __init__(self):
        pass

    def _deltas(self, errors, epsilon, mean, std):
        below = errors[errors <= epsilon]
        if not len(below):
            return 0, 0
        return mean - below.mean(), std - below.std()

    def _count_above(self, errors, epsilon):
        above = errors > epsilon
        total_above =len(errors[above])
        above = pd.Series(above)
        shift = above.shift(1)
        change = above != shift
        total_consecutive = sum(above & change)
        return total_above, total_consecutive

    def _z_cost(self, z, errors, mean, std):
        epsilon = mean + z * std
        delta_mean, delta_std =self._deltas(errors, epsilon, mean, std)
        above, consecutive =self._count_above(errors, epsilon)
        numerator =-(delta_mean / mean + delta_std / std)
        denominator = above + consecutive **2
        if denominator ==0:
            return np.inf
        return numerator / denominator

    def _find_threshold(self, errors, z_range):

        mean = errors.mean()
        std = errors.std()
        min_z, max_z = z_range
        best_z = min_z
        best_cost = np.inf
        for z in range(min_z, max_z):
            best = np.fmin(self._z_cost, z, args=(errors, mean, std), full_output=True, disp=False)
            z, cost = best[0:2]
            if cost < best_cost:
                best_z = z[0]
        return mean + best_z * std

    def _fixed_threshold(self, errors, k=3.0):
        mean = errors.mean()
        std = errors.std()
        return mean + k * std

    def _find_sequences(self, errors, epsilon, anomaly_padding):
        above = pd.Series(errors > epsilon)
        index_above = np.argwhere(above.values)
        for idx in index_above.flatten():
            above[max(0, idx - anomaly_padding):min(idx + anomaly_padding +1, len(above))] =True
        shift = above.shift(1).fillna(False)
        change = above != shift
        if above.all():
            max_below =0
        else:
            max_below = max(errors[~above])
        index = above.index
        starts = index[above & change].tolist()
        ends = (index[~above & change]-1).tolist()
        if len(ends) ==len(starts)-1:
            ends.append(len(above)-1)
        return np.array([starts, ends]).T, max_below


    def _get_max_errors(self, errors, sequences, max_below):
        max_errors = [{'max_error': max_below, 'start': -1, 'stop': -1}]
        for sequence in sequences:
            start, stop = sequence
            sequence_errors = errors[start: stop +1]
            max_errors.append({'start': start, 'stop': stop, 'max_error': max(sequence_errors)})
        max_errors = pd.DataFrame(max_errors).sort_values('max_error', ascending=False)
        return max_errors.reset_index(drop=True)


    def _prune_anomalies(self, max_errors, min_percent):
        next_error = max_errors['max_error'].shift(-1).iloc[:-1]
        max_error = max_errors['max_error'].iloc[:-1]
        increase = (max_error-next_error) / max_error
        too_small = increase < min_percent
        if too_small.all():
            last_index =-1
        else:
            last_index = max_error[~too_small].index[-1]
        return max_errors[['start', 'stop', 'max_error']].iloc[0: last_index+1].values

    def _compute_scores(self, pruned_anomalies, errors, threshold, window_start):

        anomalies = list()
        denominator = errors.mean() + errors.std()
        for row in pruned_anomalies:
            max_error = row[2]
            score = (max_error-threshold) / denominator
            anomalies.append([row[0]+window_start, row[1]+window_start, score])
        return anomalies

    def _merge_sequences(self, sequences):
        if len(sequences) == 0:
            return np.array([])
        sorted_sequences = sorted(sequences, key=lambda entry: entry[0])
        new_sequences = [sorted_sequences[0]]
        score = [sorted_sequences[0][2]]
        weights = [sorted_sequences[0][1] - sorted_sequences[0][0]]
        for sequence in sorted_sequences[1:]:
            prev_sequence = new_sequences[-1]
            if sequence[0] <= prev_sequence[1] +1:
                score.append(sequence[2])
                weights.append(sequence[1] - sequence[0])
                weighted_average = np.average(score, weights=weights)
                new_sequences[-1] = (prev_sequence[0], max(prev_sequence[1], sequence[1]), weighted_average)
            else:
                score = [sequence[2]]
                weights = [sequence[1] - sequence[0]]
                new_sequences.append(sequence)
        return np.array(new_sequences)

    def _find_window_sequences(self, window, z_range, anomaly_padding, min_percent, window_start, fixed_threshold):
        if fixed_threshold:threshold =self._fixed_threshold(window)
        else:
            threshold =self._find_threshold(window, z_range)
        window_sequences, max_below =self._find_sequences(window, threshold, anomaly_padding)
        max_errors =self._get_max_errors(window, window_sequences, max_below)
        pruned_anomalies = self._prune_anomalies(max_errors, min_percent)
        window_sequences = self._compute_scores(pruned_anomalies, window, threshold, window_start)
        return window_sequences

    def find_anomalies(self, errors, index, z_range=(0, 10), window_size=None, window_size_portion=None, window_step_size=None,
window_step_size_portion=None, min_percent=0.1, anomaly_padding=50, lower_threshold=False, fixed_threshold=True):

        window_size = window_size or len(errors)
        if window_size_portion:
            window_size = np.ceil(len(errors) * window_size_portion).astype('int')
        window_step_size = window_step_size or window_size
        if window_step_size_portion:
            window_step_size = np.ceil(window_size*window_step_size_portion).astype('int')
        window_start =0
        window_end =0
        sequences = list()

        while window_end <len(errors):
            window_end = window_start + window_size
            window = errors[window_start:window_end]
            window_sequences =self._find_window_sequences(window, z_range, anomaly_padding, min_percent, window_start, fixed_threshold)
            sequences.extend(window_sequences)
            if lower_threshold:
                # Flip errors sequence around mean
                mean = window.mean()
                inverted_window = mean - (window - mean)
                inverted_window_sequences=self._find_window_sequences(inverted_window,
                z_range,
                anomaly_padding,
                min_percent,
                window_start,
                fixed_threshold)
                sequences.extend(inverted_window_sequences)
            window_start = window_start + window_step_size

        sequences =self._merge_sequences(sequences)
        anomalies = list()
        for start, stop, score in sequences:
            # print("start", start)
            # print("stop", stop)
            # print("score", score)
            anomalies.append([index[int(start)], index[int(stop)], score])
        return anomalies

    def _compute_critic_score(self, critics, smooth_window):
        """Compute an array of anomaly scores.
        Args:
        critics (ndarray): Critic values.
        smooth_window (int): Smooth window that will be applied to compute smooth errors.
        Returns:
        ndarray: Array of anomaly scores.
        """
        critics = np.asarray(critics)
        l_quantile = np.quantile(critics, 0.25)
        u_quantile = np.quantile(critics, 0.75)
        in_range = np.logical_and(critics >= l_quantile, critics <= u_quantile)
        critic_mean = np.mean(critics[in_range])
        critic_std = np.std(critics)
        z_scores = np.absolute((np.asarray(critics) - critic_mean) / critic_std) +1
        z_scores = pd.Series(z_scores).rolling(smooth_window, center=True,
            min_periods=smooth_window //2).mean().values
        return z_scores

    def _regression_errors(y, y_hat, smoothing_window=0.01, smooth=True):
        """Compute an array of absolute errors comparing predictions and expected output.
        If smooth is True, apply EWMA to the resulting array of errors.
        Args:
        y (ndarray): Ground truth.
        y_hat (ndarray): Predicted values.
        smoothing_window (float):
        Optional. Size of the smoothing window, expressed as a proportion of the total
        length of y. If not given, 0.01 is used.
        smooth (bool):
        Optional. Indicates whether the returned errors should be smoothed with EWMA.
        If not given, `True` is used.
        Returns:
        ndarray: Array of errors.
        """
        errors = np.abs(y-y_hat)[:, 0]
        if not smooth:
            return errors
        smoothing_window =int(smoothing_window*len(y))
        return pd.Series(errors).ewm(span=smoothing_window).mean().values


    def _point_wise_error(self, y, y_hat):
        """Compute point-wise error between predicted and expected values.
        Args:
        y (ndarray): Ground truth.
        y_hat (ndarray): Predicted values.
        Returns:
        ndarray: An array of smoothed point-wise error.
        """
        y_abs = abs(y-y_hat)
        y_abs_sum = np.sum(y_abs, axis=-1)
        return y_abs_sum

    def _area_error(self, y, y_hat, score_window =10):
        smooth_y = pd.Series(y).rolling(score_window, center=True, min_periods = score_window //2).apply(integrate.trapz)
        smooth_y_hat = pd.Series(y).rooling(score_window, center = True, min_periods = score_window //2).apply(integrate.trapz)
        errors = abs(smooth_y - smooth_y_hat)
        return errors

  #여기서부터 indent확인하
    def _dtw_error(self, y, y_hat, score_window=10):
        """Compute dtw error between predicted and expected values.
        Args:
        y (ndarray): Ground truth.
        y_hat (ndarray): Predicted values.
        score_window (int):
        Optional. Size of the window over which the scores are calculated.
        If not given, 10 is used.
        Returns:
        ndarray: An array of dtw error.
        """
        length_dtw = (score_window //2) *2 +1
        half_length_dtw = length_dtw //2
        # add padding
        y_pad = np.pad(y, (half_length_dtw, half_length_dtw), 'constant', constant_values=(0, 0))
        y_hat_pad = np.pad(y_hat, (half_length_dtw, half_length_dtw), 'constant', constant_values=(0, 0))
        i = 0
        similarity_dtw = list()
        while i <len(y)-length_dtw:
            true_data = y_pad[i:i+length_dtw]
            true_data = true_data.flatten()
            pred_data = y_hat_pad[i:i+length_dtw]
            pred_data = pred_data.flatten()
            dist = dtw(true_data, pred_data)
            similarity_dtw.append(dist)
            i +=1
        errors = ([0] * half_length_dtw + similarity_dtw + [0] * (len(y)-len(similarity_dtw) - half_length_dtw))
        return errors



    def _reconstruction_errors(self, y, y_hat, step_size=1, score_window=10, smoothing_window=0.01, smooth=True, rec_error_type='point'):


        if isinstance(smoothing_window, float):
            smoothing_window = min(math.trunc(len(y) * smoothing_window), 200)
        true=[]
        for i in range(len(y)):
            true.append(y[i][0])
        for it in range(len(y[-1]) -1): # contents of the last window included
            true.append(y[-1][it+1])
        # anomalies.py (16-2)

        predictions = []
        predictions_vs = []
        pred_length = y_hat.shape[1]
        num_errors = y_hat.shape[1] + step_size * (y_hat.shape[0] -1)
        for i in range(num_errors):
            intermediate = []
            for j in range(max(0, i - num_errors + pred_length), min(i+1, pred_length)):
                intermediate.append(y_hat[i-j, j])
            ave_p = []
            if intermediate:
                predictions.append(np.average(intermediate, axis=0))
                predictions_vs.append([[
                    np.min(np.asarray(intermediate)),
                    np.percentile(np.asarray(intermediate), 25),
                    np.percentile(np.asarray(intermediate), 50),
                    np.percentile(np.asarray(intermediate), 75),
                    np.max(np.asarray(intermediate))
                ]])
        true = np.asarray(true)
        predictions = np.asarray(predictions)
        predictions_vs = np.asarray(predictions_vs)
        # Compute reconstruction errors
        if rec_error_type.lower() =="point":
            errors =self._point_wise_error(true, predictions)
        elif rec_error_type.lower() =="area":
            errors =self._area_error(true, predictions, score_window)
        elif rec_error_type.lower() =="dtw":
            errors =self._dtw_error(true, predictions, score_window)

        # Apply smoothing
        if smooth:
            errors = pd.Series(errors).rolling(smoothing_window,
                                        center=True, min_periods=smoothing_window //2).mean().values
        return errors, predictions_vs


    def score_anomalies(self, y, y_hat, critic, index,
            score_window=10, critic_smooth_window=None,
            error_smooth_window=None, smooth=True,
            rec_error_type="point", comb="mult", lambda_rec=0.5):

        critic_smooth_window = critic_smooth_window or math.trunc(y.shape[0]*0.01)
        error_smooth_window = error_smooth_window or math.trunc(y.shape[0]*0.01)
        step_size =1 # expected to be 1
        true_index = list(index) # no offset
        true = []
        for i in range(len(y)):
            true.append(y[i][0])
        for it in range(len(y[-1]) -1):  # contents of the last window included
            true.append(y[-1][it+1])
            true_index.append((index[-1] + it +1)) # extend the index (by inluding the last window part)
        true_index = np.array(true_index)# in order to cover the whole sequence of data
        critic_extended = list()
        for c in critic:
            critic_extended.extend(np.repeat(c, y_hat.shape[1]).tolist())
        critic_extended = np.asarray(critic_extended).reshape((-1, y_hat.shape[1]))
        critic_kde_max = []
        pred_length = y_hat.shape[1]
        num_errors = y_hat.shape[1] + step_size * (y_hat.shape[0]-1)

        for i in range(num_errors):
            critic_intermediate = []
            for j in range(max(0, i - num_errors + pred_length), min(i+1, pred_length)):
                critic_intermediate.append(critic_extended[i - j, j])
            if len(critic_intermediate) >1:
                discr_intermediate = np.asarray(critic_intermediate)
                try:
                    critic_kde_max.append(discr_intermediate[np.argmax(stats.gaussian_kde(discr_intermediate)(critic_intermediate))])
                except np.linalg.LinAlgError:
                    critic_kde_max.append(np.median(discr_intermediate))
            else:
                critic_kde_max.append(np.median(np.asarray(critic_intermediate)))

        # Compute critic scores
        critic_scores =self._compute_critic_score(critic_kde_max, critic_smooth_window)
        # Compute reconstruction scores
        rec_scores, predictions =self._reconstruction_errors(y, y_hat, step_size, score_window, error_smooth_window, smooth, rec_error_type)
        rec_scores = stats.zscore(rec_scores)
        rec_scores = np.clip(rec_scores, a_min=0, a_max=None) +1
        # Combine the two scores
        if comb =="mult":
            final_scores = np.multiply(critic_scores, rec_scores)
        elif comb =="sum":
            final_scores = (1 - lambda_rec) * (critic_scores -1) + lambda_rec * (rec_scores -1)
        elif comb =="rec":
            final_scores = rec_scores
        else:
            raise ValueError('Unknown combination specified {}, use "mult", "sum", or "rec" instead.'.format(comb))
        true = [[t] for t in true]
        return final_scores, true_index, true, predictions