# -*- coding: utf-8 -*-

"""twaml.data module

This module contains a classe to abstract datasets using
pandas.DataFrames as the payload for feeding to machine learning
frameworks and other general data investigating

"""

import uproot
import pandas as pd
import h5py
import numpy as np
import re
import yaml
from pathlib import PosixPath
from typing import List, Dict, Tuple, Optional, Union
import logging

log = logging.getLogger(__name__)

__all__ = ["dataset", "scale_weight_sum"]


class dataset:
    """A class to define a dataset with a pandas.DataFrame as the payload
    of the class. The class provides a set of static functions to
    construct a dataset. The class constructor should be used only in
    very special cases.

    ``datasets`` should `always` be constructed from a staticmethod,
    currently there are 3 available:

      - :meth:`dataset.from_root`
      - :meth:`dataset.from_pytables`
      - :meth:`dataset.from_h5`

    Attributes
    ----------
    files: List[PosixPath]
      List of files delivering the dataset
    name: str
      Name for the dataset
    tree_name: str
      All of our datasets had to come from a ROOT tree at some
      point. This is the name
    weights: numpy.ndarray
      The array of event weights
    df: pandas.DataFrame
      The payload of the class, a dataframe
    extra_weights: Optional[pandas.DataFrame]
      Extra weights to have access too
    label: Optional[int]
      Optional dataset label (as an int)
    auxlabel: Optional[int]
      Optional auxiliary label (as an int) - sometimes we need two labels
    label_asarray: Optional[np.ndarray]
      Optional dataset label (as an array of ints)
    auxlabel_asarray: Optional[np.ndarray]
      Optional dataset auxiliary label (as an array of ins)
    has_payload: bool
      Flag to know that the dataset actually wraps data
    cols: List[str]
      Column names as a list of strings
    shape: Tuple
      Shape of the main payload dataframe
    wtmetas: Optional[Dict[str, Dict[str]]]
      A dictionary of files to meta dictionaries

    """

    _weights = None
    _df = None
    _extra_weights = None
    files = None
    name = None
    weight_name = None
    tree_name = None
    _label = None
    _auxlabel = None
    wtmetas = None

    def _init(
        self,
        input_files: List[str],
        name: Optional[str] = None,
        tree_name: str = "WtLoop_nominal",
        weight_name: str = "weight_nominal",
        label: Optional[int] = None,
        auxlabel: Optional[int] = None,
    ) -> None:
        """Default initialization - should only be called by internal
        staticmethods ``from_root``, ``from_pytables``, ``from_h5``

        Parameters
        ----------
        input_files: List[str]
          List of input files
        name: Optional[str]
          Name of the dataset (if none use first file name)
        tree_name: str
          Name of tree which this dataset originated from
        weight_name: str
          Name of the weight branch
        label: Optional[int]
          Give dataset an integer based label
        auxlabel: Optional[int]
          Give dataset an integer based auxiliary label
        """
        self._weights = np.array([])
        self._df = pd.DataFrame({})
        self._extra_weights = None
        self.files = [PosixPath(f) for f in input_files]
        for f in self.files:
            assert f.exists(), f"{f} does not exist"
        if name is None:
            self.name = str(self.files[0].parts[-1])
        else:
            self.name = name
        self.weight_name = weight_name
        self.tree_name = tree_name
        self._label = label
        self._auxlabel = auxlabel

    @staticmethod
    def _combine_wtmetas(meta1, meta2) -> Optional[dict]:
        if meta1 is not None and meta2 is not None:
            return {**meta1, **meta2}
        elif meta1 is None and meta2 is not None:
            return {**meta2}
        elif meta1 is not None and meta2 is None:
            return {**meta1}
        else:
            return None

    @property
    def has_payload(self) -> bool:
        has_df = not self._df.empty
        has_weights = self._weights.shape[0] > 0
        return has_df and has_weights

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, new: pd.DataFrame) -> None:
        assert len(new) == len(self._weights), "df length != weight length"
        self._df = new

    @property
    def weights(self) -> np.ndarray:
        return self._weights

    @weights.setter
    def weights(self, new: np.ndarray) -> None:
        assert len(new) == len(self._df), "weight length != frame length"
        self._weights = new

    @property
    def extra_weights(self) -> pd.DataFrame:
        return self._extra_weights

    @extra_weights.setter
    def extra_weights(self, new: pd.DataFrame) -> None:
        if new is not None:
            assert len(new) == len(self._df), "extra_weights length != frame length"
        self._extra_weights = new

    @property
    def label(self) -> Optional[int]:
        return self._label

    @label.setter
    def label(self, new: int) -> None:
        self._label = new

    @property
    def label_asarray(self) -> Optional[np.ndarray]:
        if self._label is None:
            return None
        return np.ones_like(self.weights, dtype=np.int64) * self._label

    @property
    def auxlabel(self) -> Optional[int]:
        return self._auxlabel

    @auxlabel.setter
    def auxlabel(self, new: int) -> None:
        self._auxlabel = new

    @property
    def auxlabel_asarray(self) -> Optional[np.ndarray]:
        if self._auxlabel is None:
            return None
        return np.ones_like(self.weights, dtype=np.int64) * self._auxlabel

    @property
    def cols(self) -> List[str]:
        return list(self.df.columns)

    @property
    def shape(self) -> Tuple:
        """Get shape of dataset (shortcut to pd.DataFrame.shape)"""
        return self.df.shape

    @shape.setter
    def shape(self, new) -> None:
        raise NotImplementedError("Cannot set shape manually")

    def _set_df_and_weights(
        self, df: pd.DataFrame, w: np.ndarray, extra: Optional[pd.DataFrame] = None
    ) -> None:
        assert len(df) == len(w), "unequal length df and weights"
        self._df = df
        self._weights = w
        if extra is not None:
            assert len(df) == len(extra), "unequal length df and extra weights"
            self._extra_weights = extra

    def keep_columns(self, cols: List[str]) -> None:
        """Drop all columns not included in ``cols``

        Parameters
        ----------
        cols: List[str]
          Columns to keep
        """
        self._df = self._df[cols]

    def keep_weights(self, weights: List[str]) -> None:
        """Drop all columns from the extra weights frame that are not in
        ``weights``

        Parameters
        ----------
        weights: List[str]
          Weights to keep in the extra weights frame
        """
        self._extra_weights = self._extra_weights[weights]

    def rm_weight_columns(self) -> None:
        """Remove all payload df columns which begin with ``weight_``

        If you are reading a dataset that was created retaining
        weights in the main payload, this is a useful function to
        remove them. The design of ``twaml.data.dataset`` expects
        weights to be separated from the payload's main dataframe.

        Internally this is done by calling
        ``pd.DataFrame.drop(..., inplace=True)`` on the payload

        """
        import re

        pat = re.compile("^weight_")
        rmthese = [c for c in self._df.columns if re.match(pat, c)]
        self._df.drop(columns=rmthese, inplace=True)

    def rmcolumns_re(self, pattern: str) -> None:
        """Remove some columns from the payload based on regex paterns

        Uses ``pd.DataFrame.drop(..., inplace=True)``.

        Parameters
        ----------
        pattern : str
          Regex used to remove columns
        """
        pat = re.compile(pattern)
        rmthese = [c for c in self._df.columns if re.search(pat, c)]
        self._df.drop(columns=rmthese, inplace=True)

    def rmcolumns(self, cols: List[str]) -> None:
        """Remove columns from the dataset

        Uses ``pd.DataFrame.drop(..., inplace=True)``.

        Parameters
        ----------
        cols: List[str]
          List of column names to remove

        """
        self._df.drop(columns=cols, inplace=True)

    def change_weights(self, wname: str) -> None:
        """Change the main weight of the dataset

        this function will swap the current main weight array of the
        dataset with one in the extra_weights frame.
        """
        assert self._extra_weights is not None, "extra weights do not exist"

        old_name = self.weight_name
        old_weights = self.weights
        self._extra_weights[old_name] = old_weights

        self.weights = self._extra_weights[wname].to_numpy()
        self.weight_name = wname

        self._extra_weights.drop(columns=[wname], inplace=True)

    def append(self, other: "dataset") -> None:

        """Append a dataset to an exiting one

        We perform concatenations of the dataframes and weights to
        update the existing dataset's payload.

        if one dataset has extra weights and the other doesn't,
        the extra weights are dropped.

        Parameters
        ----------
        other : twanaet.data.dataset
          The dataset to append

        """
        assert self.has_payload, "Unconstructed df (self)"
        assert other.has_payload, "Unconstructed df (other)"
        assert self.weight_name == other.weight_name, "different weight names"
        assert self.shape[1] == other.shape[1], "different df columns"

        if self.extra_weights is not None and other.extra_weights is not None:
            assert (
                self.extra_weights.shape[1] == other.extra_weights.shape[1]
            ), "extra weights are different lengths"

        self._df = pd.concat([self._df, other.df])
        self._weights = np.concatenate([self._weights, other.weights])
        self.files = self.files + other.files
        self.wtmetas = self._combine_wtmetas(self.wtmetas, other.wtmetas)

        if self.extra_weights is not None and other.extra_weights is not None:
            self._extra_weights = pd.concat([self._extra_weights, other.extra_weights])
        else:
            self._extra_weights = None

    def to_pytables(self, file_name: str) -> None:
        """Write payload to disk as a pytables h5 file (with a strict naming
        scheme)

        The key in the file is the name of the dataset. The weights
        array is stored as a separate frame with the key being the
        weight_name attribute. If extra weights are present they
        are saved as well.

        An existing dataset label **is not stored**.

        Parameters
        ----------
        file_name : str
          output file name,

        """
        if PosixPath(file_name).exists():
            log.warning(f"{file_name} exists, overwriting")
        weights_frame = pd.DataFrame(dict(weights=self._weights))
        self._df.to_hdf(file_name, self.name, mode="w")
        weights_frame.to_hdf(file_name, self.weight_name, mode="a")
        if self._extra_weights is not None:
            self._extra_weights.to_hdf(
                file_name, f"{self.name}_extra_weights", mode="a"
            )
        if self.wtmetas is not None:
            tempdict = {k: np.array([str(v)]) for k, v in self.wtmetas.items()}
            wtmetadf = pd.DataFrame.from_dict(tempdict)
            wtmetadf.to_hdf(file_name, "wtmetas", mode="a")

    def __add__(self, other: "dataset") -> "dataset":
        """Add two datasets together

        We perform concatenations of the dataframes and weights to
        generate a new dataset with the combined a new payload.

        if one dataset has extra weights and the other doesn't,
        the extra weights are dropped.

        """
        assert self.has_payload, "Unconstructed df (self)"
        assert other.has_payload, "Unconstructed df (other)"
        assert self.weight_name == other.weight_name, "different weight names"
        assert self.shape[1] == other.shape[1], "different df columns"

        if self.extra_weights is not None and other.extra_weights is not None:
            assert (
                self.extra_weights.shape[1] == other.extra_weights.shape[1]
            ), "extra weights are different lengths"

        new_weights = np.concatenate([self.weights, other.weights])
        new_df = pd.concat([self.df, other.df])
        new_files = [str(f) for f in (self.files + other.files)]
        new_ds = dataset()
        new_ds._init(
            new_files,
            self.name,
            weight_name=self.weight_name,
            tree_name=self.tree_name,
            label=self._label,
            auxlabel=self._auxlabel,
        )
        new_ds.wtmetas = self._combine_wtmetas(self.wtmetas, other.wtmetas)

        if self.extra_weights is not None and other.extra_weights is not None:
            new_aw = pd.concat([self.extra_weights, other.extra_weights])
        else:
            new_aw = None

        new_ds._set_df_and_weights(new_df, new_weights, extra=new_aw)
        return new_ds

    def __len__(self) -> int:
        """length of the dataset"""
        return len(self.weights)

    def __repr__(self) -> str:
        """standard repr"""
        return f"<twaml.data.dataset(name={self.name}, shape={self.shape})>"

    def __str__(self) -> str:
        """standard str"""
        return f"dataset(name={self.name})"

    @staticmethod
    def from_root(
        input_files: Union[str, List[str]],
        name: Optional[str] = None,
        tree_name: str = "WtLoop_nominal",
        weight_name: str = "weight_nominal",
        branches: List[str] = None,
        selection: Optional[str] = None,
        label: Optional[int] = None,
        auxlabel: Optional[int] = None,
        allow_weights_in_df: bool = False,
        extra_weights: Optional[List[str]] = None,
        detect_weights: bool = False,
        executor: Optional["ThreadPoolExecutor"] = None,
        wtloop_meta: bool = False,
    ) -> "dataset":
        """Initialize a dataset from ROOT files

        Parameters
        ----------
        input_files: str or List[str]
          Single or list of ROOT input file(s) to use
        name: str
          Name of the dataset (if none use first file name)
        tree_name: str
          Name of the tree in the file to use
        weight_name: str
          Name of the weight branch
        branches: List[str]
          List of branches to store in the dataset, if None use all
        selection: str
          A string passed to pandas.DataFrame.eval to apply a selection
          based on branch/column values. Column names must be prepended
          by ``df.``, e.g. ``(df.reg1j1b == True) & (df.OS == True)``
          requires the ``reg1j1b`` and ``OS`` branches to be ``True``.
        label: Optional[int]
          Give the dataset an integer label
        auxlabel: Optional[int]
          Give the dataset an integer auxiliary label
        allow_weights_in_df: bool
          Allow "^weight_" branches in the payload dataframe
        extra_weights: Optional[List[str]]
          Extra weights to store in a second dataframe.
        detect_weights: bool
          If True, fill the extra_weights df with all "^weight_"
          branches If ``extra_weights`` is not None, this option is
          ignored.
        executor: Optional[ThreadPoolExecutor]
          Fill frames using multiple threads,
          see uproot.TTreeMethods_pandas.df
        wtloop_meta: bool
          grab and store the `WtLoop_meta` YAML entries. stored as a dictionary
          of the form ``{ str(filename) : dict(yaml) }`` in the class variable
          ``wtmetas``.

        Examples
        --------
        Example with a single file and two branches:

        >>> ds1 = dataset.from_root(["file.root"], name="myds",
        ...                         branches=["pT_lep1", "pT_lep2"], label=1)

        Example with multiple input_files and a selection (uses all
        branches). The selection requires the branch ``nbjets == 1``
        and ``njets >= 1``, then label it 5.

        >>> flist = ["file1.root", "file2.root", "file3.root"]
        >>> ds = dataset.from_root(flist, selection='(df.nbjets == 1) & (df.njets >= 1)')
        >>> ds.label = 5

        Example using extra weights

        >>> ds = dataset.from_root(flist, name="myds", weight_name="weight_nominal",
        ...                        extra_weights=["weight_sys_radLo", " weight_sys_radHi"])

        Example where we detect extra weights automatically

        >>> ds = dataset.from_root(flist, name="myds", weight_name="weight_nominal",
        ...                        detect_weights=True)

        Example using an executor (16 threads):

        >>> from concurrent.futures import ThreadPoolExecutor
        >>> executor = ThreadPoolExecutor(16)
        >>> ds = dataset.from_root(flist, name="myds", executor=executor)

        """

        if isinstance(input_files, (str, bytes)):
            input_files = [input_files]
        else:
            try:
                iter(input_files)
            except TypeError:
                input_files = [input_files]
            else:
                input_files = list(input_files)

        ds = dataset()
        ds._init(
            input_files,
            name,
            tree_name=tree_name,
            weight_name=weight_name,
            label=label,
            auxlabel=auxlabel,
        )

        if wtloop_meta:
            meta_trees = {
                file_name: uproot.open(file_name)["WtLoop_meta"]
                for file_name in input_files
            }
            ds.wtmetas = {
                fn: yaml.full_load(mt.array("meta_yaml")[0])
                for fn, mt in meta_trees.items()
            }

        uproot_trees = [uproot.open(file_name)[tree_name] for file_name in input_files]

        wpat = re.compile("^weight_")
        if extra_weights is not None:
            w_branches = extra_weights
        elif detect_weights:
            urtkeys = [k.decode("utf-8") for k in uproot_trees[0].keys()]
            w_branches = [k for k in urtkeys if re.match(wpat, k)]
            if weight_name in w_branches:
                w_branches.remove(weight_name)
        else:
            w_branches = None

        frame_list, weight_list, extra_frame_list = [], [], []
        for t in uproot_trees:
            raw_w = t.array(weight_name)
            df = t.pandas.df(branches=branches, namedecode="utf-8", executor=executor)
            if not allow_weights_in_df:
                rmthese = [c for c in df.columns if re.match(wpat, c)]
                df.drop(columns=rmthese, inplace=True)

            if w_branches is not None:
                raw_aw = t.pandas.df(branches=w_branches, namedecode="utf-8")

            if selection is not None:
                iselec = pd.eval(selection)
                raw_w = raw_w[iselec]
                df = df[iselec]
                if w_branches is not None:
                    raw_aw = raw_aw[iselec]

            assert len(raw_w) == len(df), "frame length and weight length different"
            weight_list.append(raw_w)
            frame_list.append(df)
            if w_branches is not None:
                extra_frame_list.append(raw_aw)
                assert len(raw_w) == len(
                    raw_aw
                ), "aux weight length and weight length different"

        weights_array = np.concatenate(weight_list)
        df = pd.concat(frame_list)
        if w_branches is not None:
            aw_df = pd.concat(extra_frame_list)
        else:
            aw_df = None

        ds._set_df_and_weights(df, weights_array, extra=aw_df)

        return ds

    @staticmethod
    def from_pytables(
        file_name: str,
        name: str = "auto",
        tree_name: str = "WtLoop_nominal",
        weight_name: str = "weight_nominal",
        label: Optional[int] = None,
        auxlabel: Optional[int] = None,
    ) -> "dataset":
        """Initialize a dataset from pytables output generated from
        dataset.to_pytables

        The payload is extracted from the .h5 pytables files using the
        name of the dataset and the weight name. If the name of the
        dataset doesn't exist in the file you'll crash. Extra weights
        are retrieved if available.

        Parameters
        ----------
        file_name: str
          Name of h5 file containing the payload
        name: str
          Name of the dataset inside the h5 file. If ``"auto"`` (default)
          we attempt to determine the name automatically from the h5 file.
        tree_name: str
          Name of tree where dataset originated (for reference)
        weight_name: str
          Name of the weight array inside the h5 file
        label: Optional[int]
          Give the dataset an integer label
        auxlabel: Optional[int]
          Give the dataset an integer auxiliary label

        Examples
        --------

        >>> ds1 = dataset.from_pytables("ttbar.h5", "ttbar")
        >>> ds1.label = 1 ## add label dataset after the fact

        """
        if name == "auto":
            with h5py.File(file_name, "r") as f:
                keys = list(f.keys())
                dsname = keys[0]
        else:
            dsname = name

        main_frame = pd.read_hdf(file_name, dsname)
        main_weight_frame = pd.read_hdf(file_name, weight_name)
        with h5py.File(file_name, "r") as f:
            if f"{dsname}_extra_weights" in f:
                extra_frame = pd.read_hdf(file_name, f"{dsname}_extra_weights")
            else:
                extra_frame = None
        w_array = main_weight_frame.weights.to_numpy()
        ds = dataset()
        ds._init(
            [file_name],
            dsname,
            weight_name=weight_name,
            tree_name=tree_name,
            label=label,
            auxlabel=auxlabel,
        )

        with h5py.File(file_name, "r") as f:
            if "wtmetas" in f:
                wtmetas = pd.read_hdf(file_name, "wtmetas")
                ds.wtmetas = {
                    fn: yaml.full_load(wtmetas[fn].to_numpy()[0])
                    for fn in wtmetas.columns
                }

        ds._set_df_and_weights(main_frame, w_array, extra=extra_frame)
        return ds

    @staticmethod
    def from_h5(
        file_name: str,
        name: str,
        columns: List[str],
        tree_name: str = "WtLoop_nominal",
        weight_name: str = "weight_nominal",
        label: Optional[int] = None,
        auxlabel: Optional[int] = None,
    ) -> "dataset":
        """Initialize a dataset from generic h5 input (loosely expected to be
        from the ATLAS Analysis Release utility ``ttree2hdf5``

        The name of the HDF5 dataset inside the file is assumed to be
        ``tree_name``. The ``name`` argument is something *you
        choose*.

        Parameters
        ----------
        file_name: str
          Name of h5 file containing the payload
        name: str
          Name of the dataset you would like to define
        columns: List[str]
          Names of columns (branches) to include in payload
        tree_name: str
          Name of tree dataset originates from (HDF5 dataset name)
        weight_name: str
          Name of the weight array inside the h5 file
        label: Optional[int]
          Give the dataset an integer label
        auxlabel: Optional[int]
          Give the dataset an integer auxiliary label

        Examples
        --------

        >>> ds = dataset.from_h5('file.h5', 'dsname', tree_name='WtLoop_EG_RESOLUTION_ALL__1up')

        """
        ds = dataset()
        ds._init(
            [file_name],
            name=name,
            weight_name=weight_name,
            tree_name=tree_name,
            label=label,
            auxlabel=auxlabel,
        )

        f = h5py.File(file_name, mode="r")
        full_ds = f[tree_name]
        w_array = f[tree_name][weight_name]
        coldict = {}
        for col in columns:
            coldict[col] = full_ds[col]
        frame = pd.DataFrame(coldict)
        ds._set_df_and_weights(frame, w_array)
        return ds


def scale_weight_sum(to_update: "dataset", reference: "dataset") -> None:
    """
    Scale the weights of the `to_update` dataset such that the sum of
    weights are equal to the sum of weights of the `reference` dataset.

    Parameters
    ----------
    to_update : twanet.data.dataset
        dataset with weights to be scaled
    reference : twanet.data.dataset
        dataset to scale to

    """
    assert to_update.has_payload, f"{to_update} is without payload"
    assert reference.has_payload, f"{reference} is without payload"
    sum_to_update = to_update.weights.sum()
    sum_reference = reference.weights.sum()
    to_update.weights *= sum_reference / sum_to_update
