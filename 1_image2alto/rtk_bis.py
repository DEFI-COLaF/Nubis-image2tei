import click
import os
import glob
import csv
from rtk.task import ExtractPDFTask, YALTAiCommand, KrakenAltoCleanUpCommand, KrakenRecognizerCommand, ClearFileCommand
from rtk import utils


def extraction(liste_image):    
    # segmentation - analyse de la mise en page
    print("[Task] Segment")
    yaltai = YALTAiCommand(
        liste_image,
        binary="yaltai",
        device="cuda",
        yolo_model="scratch/rtk/LADaS.pt",
        verbose=True,
        raise_on_error=False,
        allow_failure=False,
        multiprocessing=8,
        check_content=False
        )
    print(yaltai)
    yaltai.process()

    # nettoyage des altos
    print("[Task] Clean-Up Serialization")
    cleanup = KrakenAltoCleanUpCommand(yaltai.output_files)
    cleanup.process()

    # OCR kraken
    print("[Task] OCR")
    kraken = KrakenRecognizerCommand(
        cleanup.output_files,
        binary="kraken",
        device="cpu",
        model="scratch/rtk/CATMuS-Gothic-Print-1.0.0.mlmodel",
        multiprocess=14,  # GPU Memory // 3gb
        check_content=True,
        raise_on_error=False
    )
    kraken.process()


@click.command()
@click.argument('csv_file', type="str")
@click.option('-n', '--number', 'number_batch', type=int, required=True, help="batch number to process")
def launch_rtk_on_batch(number_batch):
    paths_batch = []
    with open(csv_file, mode='r') as file:
        reader=csv.DictReader(file)
        for row in reader:
            if row['Batch Number'] == str(number_batch):
                paths_batch.append(row['Image Path'])
    print('Launch RTK Batch' + str(number_batch))
    print(paths_batch)
    extraction(paths_batch)

if __name__ == '__main__':
    launch_rtk_on_batch()

    
