use rand::seq::SliceRandom;
use rand::Rng;
use std::env;
use std::process::{Command, Stdio};
use std::thread;

fn run_python_script(thread_id: usize, arguments: &[String; 5]) {
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

    if args.len() != 3 {
        eprint!("Usage cargo run -- number_of_threads number_of_itterations");
        std::process::exit(1);
    }

    let mut handles = vec![];

    let number_of_threads: usize = args[1].parse().expect("Invalid number of threads number");
    let number_of_iterations: String = args[2].clone();

    let bot_options = ["minmax_stats", "prunning_stats", "random_stats"];
    let number_of_turns_option: Vec<String> = (10..=150)
    .step_by(10)
    .map(|n| n.to_string())
    .collect();

    let time_per_turn_options = ["0.5", "1.0", "1.5", "2.0"];

    let mut rng = rand::thread_rng();

    for i in 0..number_of_threads {
        let mut white_bot: String = bot_options.choose(&mut rng).unwrap().to_string();
        let mut black_bot: String = bot_options.choose(&mut rng).unwrap().to_string();

         while white_bot == "random_stats" && black_bot == "random_stats" {
            if rng.gen_bool(0.5) {
                white_bot = bot_options.choose(&mut rng).unwrap().to_string();
            } else {
                black_bot = bot_options.choose(&mut rng).unwrap().to_string();
            }
        }

        let number_of_turns: String = number_of_turns_option.choose(&mut rng).unwrap().to_string();
        let time_per_turn: String = time_per_turn_options.choose(&mut rng).unwrap().to_string();

        let iterations: String = number_of_iterations.clone();
        let options: [String; 5] = [white_bot, black_bot, number_of_turns, time_per_turn, iterations];
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
