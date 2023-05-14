#!/usr/bin/env python
"""
Download the raw dataset from W&B, apply basic data cleaning, and export the result to a new artifact.
"""

import argparse
import logging
import os

import pandas as pd
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def clean_dataset(df, min_price, max_price):
    """Apply basic data cleaning to the input DataFrame."""
    # Drop outliers
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    return df


def download_artifact(run, artifact_name):
    """Download the specified artifact from W&B and return its local path."""
    logger.info("Downloading artifact: %s", artifact_name)
    artifact = run.use_artifact(artifact_name)
    artifact_path = artifact.file()
    return artifact_path


def save_artifact(run, artifact_name, artifact_type, artifact_description, file_path):
    """Save the cleaned dataset to a new artifact in W&B."""
    logger.info("Saving output artifact: %s", artifact_name)
    artifact = wandb.Artifact(artifact_name, type=artifact_type, description=artifact_description)
    artifact.add_file(file_path)
    run.log_artifact(artifact)


def main(args):
    """Main function that runs the data cleaning pipeline."""
    # Initialize W&B run
    with wandb.init(job_type="basic_cleaning", config=args) as run:
        # Download input artifact
        artifact_path = download_artifact(run, args.input_artifact)
        df = pd.read_csv(artifact_path)

        # Clean dataset
        logger.info("Cleaning dataset")
        df = clean_dataset(df, args.min_price, args.max_price)

        # Save cleaned dataset to file
        file_name = "clean_sample.csv"
        df.to_csv(file_name, index=False)

        # Save cleaned dataset to new artifact
        save_artifact(run, args.output_artifact, args.output_type, args.output_description, file_name)

        # Remove temporary file
        os.remove(file_name)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A very basic data cleaning")
    parser.add_argument("--input_artifact", type=str, help="Fully-qualified name for the input artifact", required=True)
    parser.add_argument("--output_artifact", type=str, help="Name of the output artifact", required=True)
    parser.add_argument("--output_type", type=str, help="Type of the output artifact", required=True)
    parser.add_argument("--output_description", type=str, help="Description for the output artifact", required=True)
    parser.add_argument("--min_price", type=float, help="Minimum price for cleaning outliers", required=True)
    parser.add_argument("--max_price", type=float, help="Maximum price for cleaning outliers", required=True)
    args = parser.parse_args()

    # Run data cleaning pipeline
    main(args)