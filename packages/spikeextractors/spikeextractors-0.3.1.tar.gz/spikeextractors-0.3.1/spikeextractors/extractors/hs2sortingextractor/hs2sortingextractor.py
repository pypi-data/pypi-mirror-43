from spikeextractors import SortingExtractor

import numpy as np

def _load_required_modules():
    try:
        import h5py
    except ModuleNotFoundError:
        raise ModuleNotFoundError("To use the BiocamRecordingExtractor install h5py: \n\n"
                                  "pip install h5py\n\n")
    return h5py


class HS2SortingExtractor(SortingExtractor):
    def __init__(self, recording_file):
        h5py = _load_required_modules()
        SortingExtractor.__init__(self)
        self._recording_file = recording_file
        self._rf = h5py.File(self._recording_file, mode='r')
        self._unit_ids = set(self._rf['cluster_id'][()])
        if 'centres' in self._rf.keys():
            self._unit_locs = self._rf['centres'][()]  # cache for faster access
            for unit_id in self._unit_ids:
                self.setUnitProperty(unit_id, 'unit_location', self._unit_locs[unit_id])
        if 'data' in self._rf.keys():
            for unit_id in self._unit_ids:
                self.setUnitSpikeFeatures(unit_id, 'spike_locations', self._rf['data'][:2, self.get_unit_indices(unit_id)].T)
        if 'ch' in self._rf.keys():
            for unit_id in self._unit_ids:
                self.setUnitSpikeFeatures(unit_id, 'spike_max_channels', np.asarray(self._rf['ch'])[self.get_unit_indices(unit_id)])

    def get_unit_indices(self, x):
        return np.where(self._rf['cluster_id'][()] == x)[0]

    def getUnitIds(self):
        return list(self._unit_ids)

    def getUnitSpikeTrain(self, unit_id, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = 0
        if end_frame is None:
            end_frame = np.Inf
        times = self._rf['times'][()][self.get_unit_indices(unit_id)]
        inds = np.where((start_frame <= times) & (times < end_frame))
        return times[inds]

    @staticmethod
    def writeSorting(sorting, save_path):
        h5py = _load_required_modules()
        unit_ids = sorting.getUnitIds()
        times_list = []
        labels_list = []
        for i in range(len(unit_ids)):
            unit = unit_ids[i]
            times = sorting.getUnitSpikeTrain(unit_id=unit)
            times_list.append(times)
            labels_list.append(np.ones(times.shape, dtype=int) * unit)
        all_times = np.concatenate(times_list)
        all_labels = np.concatenate(labels_list)
        rf = h5py.File(save_path, mode='w')
        # for now only create the entries required by any RecordingExtractor
        rf.create_dataset("times", data=all_times)
        rf.create_dataset("cluster_id", data=all_labels)
        rf.close()
