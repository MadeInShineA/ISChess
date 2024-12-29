use rand::seq::SliceRandom;
use std::env;
use std::process::{Command, Stdio};
use std::thread;

fn run_python_script(thread_id: usize, arguments: &[&str; 4]) {
    println!("Thread {}: Starting Python script", thread_id);

    let status = Command::new("venv/bin/python") // Use full path to Python
        .arg("AB_stats.py") // Use correct path to the script
        .args(arguments)
        .current_dir("../") // Set the working directory
        .stdout(Stdio::inherit()) // Forward stdout
        .stderr(Stdio::inherit()) // Forward stderr
        .status(); // Execute command

    match status {
        Ok(status) if status.success() => {
            println!("Thread {}: AB_stats.py executed successfully", thread_id)
        }
        Ok(status) => eprintln!(
            "Thread {}: AB_stats.py failed with status: {}",
            thread_id, status
        ),
        Err(e) => eprintln!("Thread {}: Failed to execute AB_stats.py: {}", thread_id, e),
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        eprint!("Usage cargo run -- NUMBER_OF_THREADS");
        std::process::exit(1);
    }

    let mut handles = vec![];

    let number_of_threads: usize = args[1].parse().expect("Invalid NUMBER_OF_THREADS value");

    let bot_options = ["minmax_stats", "prunning_stats"];
    let number_of_turns_option = ["5", "10", "15"];
    let time_per_turn_options = ["0.5", "1.0", "1.5", "2.0"];

    let mut rng = rand::thread_rng();

    for i in 0..number_of_threads {
        let white_bot: &str = bot_options.choose(&mut rng).unwrap();
        let black_bot: &str = bot_options.choose(&mut rng).unwrap();
        let number_of_turns: &str = number_of_turns_option.choose(&mut rng).unwrap();
        let time_per_turn: &str = time_per_turn_options.choose(&mut rng).unwrap();

        let options: [&str; 4] = [white_bot, black_bot, number_of_turns, time_per_turn];
        let handle = thread::spawn(move || {
            run_python_script(i, &options);
        });
        handles.push(handle);
    }

    // Wait for all threads to finish
    for handle in handles {
        handle.join().expect("Thread panicked");
    }
}
