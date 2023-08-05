#!/usr/bin/env python
# Copyright (C) 2019 Emanuel Goncalves

import os
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from crispy.Utils import Utils
from crispy import dpath, logger
from crispy.QCPlot import QCplot


class Sample:
    """
    Import module that handles the sample list (i.e. list of cell lines) and their descriptive information.

    """

    def __init__(
        self, index="model_id", samplesheet_file="model_list_2018-09-28_1452.csv"
    ):
        self.index = index

        # Import samplesheet
        self.samplesheet = (
            pd.read_csv(f"{dpath}/{samplesheet_file}")
            .dropna(subset=[self.index])
            .set_index(self.index)
        )


class GeneExpression:
    """
    Import module of gene-expression data-set.

    """

    def __init__(
        self, voom_file="gexp/rnaseq_voom.csv.gz", rpkm_file="gexp/rnaseq_rpkm.csv.gz"
    ):
        self.voom = pd.read_csv(f"{dpath}/{voom_file}", index_col=0)
        self.rpkm = pd.read_csv(f"{dpath}/{rpkm_file}", index_col=0)

    def get_data(self, dtype="voom"):
        if dtype.lower() == "rpkm":
            return self.rpkm.copy()

        else:
            return self.voom.copy()

    def filter(self, dtype="voom", subset=None):
        df = self.get_data(dtype=dtype)

        # Subset matrices
        if subset is not None:
            df = df.loc[:, df.columns.isin(subset)]

        return df

    def is_not_expressed(self, rpkm_threshold=1, subset=None):
        rpkm = self.filter(dtype="rpkm", subset=subset)
        rpkm = (rpkm < rpkm_threshold).astype(int)
        return rpkm


class CRISPRComBat:
    """
    Import module of Sanger + Broad CRISPR-Cas9 cancer cell lines screens.

    """

    LOW_QUALITY_SAMPLES = ["SIDM00096", "SIDM01085", "SIDM00958"]

    def __init__(
        self,
        dmatrix_file="InitialCombat_BroadSanger_Matrix.csv.gz",
        dmatrix_original_file="InitialCombat_BroadSanger.csv.gz",
    ):
        self.ss = Sample()
        self.datadir = f"{dpath}/crispr/"
        self.dmatrix_file = dmatrix_file

        if not os.path.exists(f"{self.datadir}/{self.dmatrix_file}"):
            logger.log(logging.INFO, "Creating merged matrix")
            self.__generate_merged_matrix(dmatrix_original_file)

            logger.log(logging.INFO, "QC recall curves of merged matrix")
            self.__qc_recall_curves()

        else:
            self.crispr = pd.read_csv(
                f"{self.datadir}/{self.dmatrix_file}", index_col=0
            )

    def __generate_merged_matrix(self, dmatrix_file):
        df = pd.read_csv(f"{self.datadir}/{dmatrix_file}", index_col=0)

        # Split Sanger matrix
        idmap_sanger = (
            self.ss.samplesheet.reset_index()
            .dropna(subset=["model_name"])
            .set_index("model_name")
        )
        crispr_sanger = df[
            [i for i in df if i in self.ss.samplesheet["model_name"].values]
        ]
        crispr_sanger = crispr_sanger.rename(columns=idmap_sanger["model_id"])

        # Split Broad matrix
        idmap_broad = (
            self.ss.samplesheet.reset_index()
            .dropna(subset=["model_name"])
            .set_index("BROAD_ID")
        )
        crispr_broad = df[
            [i for i in df if i in self.ss.samplesheet["BROAD_ID"].values]
        ]
        crispr_broad = crispr_broad.rename(columns=idmap_broad["model_id"])

        # Merge matrices
        self.crispr = pd.concat(
            [
                crispr_sanger,
                crispr_broad[[i for i in crispr_broad if i not in crispr_sanger]],
            ],
            axis=1,
            sort=False,
        ).dropna()
        self.crispr.to_csv(
            f"{self.datadir}/InitialCombat_BroadSanger_Matrix.csv.gz",
            compression="gzip",
        )

        # Store isntitute sample origin
        institute = pd.Series(
            {s: "Sanger" if s in crispr_sanger else "Broad" for s in self.crispr}
        )
        institute.to_csv(
            f"{self.datadir}/InitialCombat_BroadSanger_Institute.csv.gz",
            compression="gzip",
        )

    def __qc_recall_curves(self):
        qc_ess = pd.Series(
            {
                i: QCplot.recall_curve(self.crispr[i], Utils.get_essential_genes())[2]
                for i in self.crispr
            }
        )
        qc_ess.to_csv(
            f"{self.datadir}/InitialCombat_BroadSanger_Essential_AURC.csv.gz",
            compression="gzip",
        )

        qc_ness = pd.Series(
            {
                i: QCplot.recall_curve(self.crispr[i], Utils.get_non_essential_genes())[
                    2
                ]
                for i in self.crispr
            }
        )
        qc_ness.to_csv(
            f"{self.datadir}/InitialCombat_BroadSanger_NonEssential_AURC.csv.gz",
            compression="gzip",
        )

    def get_data(self, scale=True, drop_lowquality=True):
        df = self.crispr.copy()

        if drop_lowquality:
            df = df.drop(columns=self.LOW_QUALITY_SAMPLES)

        if scale:
            df = self.scale(df)

        return df

    def filter(
        self,
        subset=None,
        scale=True,
        abs_thres=None,
        drop_core_essential=False,
        min_events=5,
        drop_core_essential_broad=False,
    ):
        df = self.get_data(scale=True)

        # - Filters
        # Subset matrices
        if subset is not None:
            df = df.loc[:, df.columns.isin(subset)]

        # Filter by scaled scores
        if abs_thres is not None:
            df = df[(df.abs() > abs_thres).sum(1) >= min_events]

        # Filter out core essential genes
        if drop_core_essential:
            df = df[~df.index.isin(Utils.get_adam_core_essential())]

        if drop_core_essential_broad:
            df = df[~df.index.isin(Utils.get_broad_core_essential())]

        # - Subset matrices
        return self.get_data(scale=scale).loc[df.index].reindex(columns=df.columns)

    @staticmethod
    def scale(df, essential=None, non_essential=None, metric=np.median):
        if essential is None:
            essential = Utils.get_essential_genes(return_series=False)

        if non_essential is None:
            non_essential = Utils.get_non_essential_genes(return_series=False)

        assert (
            len(essential.intersection(df.index)) != 0
        ), "DataFrame has no index overlapping with essential list"

        assert (
            len(non_essential.intersection(df.index)) != 0
        ), "DataFrame has no index overlapping with non essential list"

        essential_metric = metric(df.reindex(essential).dropna(), axis=0)
        non_essential_metric = metric(df.reindex(non_essential).dropna(), axis=0)

        df = df.subtract(non_essential_metric).divide(
            non_essential_metric - essential_metric
        )

        return df
