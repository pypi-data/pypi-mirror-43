from imageatm.components import DataPrep


def run_data_prep(image_dir, samples_file, job_dir, resize, **kwargs):

    dp = DataPrep(job_dir=job_dir, image_dir=image_dir, samples_file=samples_file)
    dp.prepare_data(resize=resize)
