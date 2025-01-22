#!/bin/bash

STATUS_FILE="./status_bis.txt"
LOG_FILE="./log_rtk_bis.txt"


is_job_running() {
    # Get the list of jobs, excluding the header
    job_list=$(squeue -u jjanes | awk 'NR>1')

    # Check if squeue returned any jobs excluding the header
    if [[ -n "$job_list" ]]; then
        # Print job list for debugging purposes
        echo "$job_list"
        return 0  # Jobs are running
    else
        echo "No jobs found or only header present."  # Debugging message
        return 1  # No jobs running
    fi
}

# Function to get the next batch number to process
get_next_batch() {
    if [ ! -f "$STATUS_FILE" ]; then
        echo 1 > "$STATUS_FILE"  # Start with batch 1 if status file doesn't exist
    fi
    cat "$STATUS_FILE"
}

update_status_file() {
    # Check if the status file exists and is readable
    if [[ -f "$STATUS_FILE" && -r "$STATUS_FILE" ]]; then
        # Read the current batch number from the status file
        current_batch=$(cat "$STATUS_FILE")

        # Check if the current batch number is a valid integer
        if [[ "$current_batch" =~ ^[0-9]+$ ]]; then
            # Increment the batch number
            next_batch=$((current_batch + 1))

            # Update the status file with the next batch number
            echo "$next_batch" > "$STATUS_FILE"
            echo "Batch number updated to $next_batch."
        else
            echo "Error: The current batch number is not a valid integer." >&2
        fi
    else
        echo "Error: Status file does not exist or is not readable." >&2
    fi
}

#check if a job is running
if is_job_running; then
    echo "$(date): Job is still running. No action taken." >> "$LOG_FILE"
    exit 0
else
    # Get the next batch number to process
    batch_num=$(get_next_batch)
    echo $batch_num
    update_status_file
fi
cat <<END >rtk_automatic.sbatch
#!/bin/bash
#
# rtk_automatic.sbatch
#

#SBATCH --job-name=rtk_bis_$batch_num

#SBATCH --ntasks=1

#SBATCH --cpus-per-task=14

#SBATCH --mem=80G

#SBATCH --partition=gpu
 
#SBATCH --gres=gpu:rtx8000:1

#SBATCH --time=1:00:00

#SBATCH --output=./logs/%x_%j.log  # Standard output and error log. %x denotes the job name, %j the jobid.

#SBATCH --mail-type=ALL

#SBATCH --mail-user=juliette.janes@inria.fr

source ~/miniconda3/etc/profile.d/conda.sh
conda activate venv-rtk
python3 scratch/rtk/rtk_bis.py -n $batch_num
END
# Check if the job script was created successfully
if [[ -f "./rtk_automatic.sbatch" ]]; then
   echo "Fichier batch créé"
   sbatch ./rtk_automatic.sbatch
   echo "$(date): Job launch $batch_nums" >> "$LOG_FILE"
else
   echo "Erreur: Le fichier de job n'a pas été créé." >&2
   exit 1
fi

