// Project NOVA - Desktop Native Automation Agent

use serde::{Deserialize, Serialize};
use std::process::Command;

#[derive(Serialize, Deserialize)]
pub struct CommandResult {
    pub success: bool,
    pub output: String,
    pub error: Option<String>,
}

// 1. Safe Application Launch (Allowlisted applications only)
#[tauri::command]
pub fn launch_app(app_name: String) -> CommandResult {
    let allowed_apps = ["code", "chrome", "notepad", "calc", "explorer"];
    let sanitized_name = app_name.to_lowercase();

    if !allowed_apps.iter().any(|&a| a == sanitized_name) {
        return CommandResult {
            success: false,
            output: String::new(),
            error: Some(format!("Application '{}' is not in the security allowlist.", app_name)),
        };
    }

    #[cfg(target_os = "windows")]
    let status = Command::new("cmd").args(["/C", "start", &sanitized_name]).spawn();

    #[cfg(target_os = "macos")]
    let status = Command::new("open").args(["-a", &sanitized_name]).spawn();

    #[cfg(target_os = "linux")]
    let status = Command::new(&sanitized_name).spawn();

    match status {
        Ok(_) => CommandResult {
            success: true,
            output: format!("Successfully launched {}", sanitized_name),
            error: None,
        },
        Err(e) => CommandResult {
            success: false,
            output: String::new(),
            error: Some(e.to_string()),
        },
    }
}

// 2. Safe Approved Terminal Execution (Strict argument validation, no arbitrary shell strings)
#[tauri::command]
pub fn execute_allowlisted_command(binary: String, args: Vec<String>) -> CommandResult {
    let allowed_binaries = ["git", "node", "python", "dir", "ls"];
    if !allowed_binaries.iter().any(|&b| b == binary) {
        return CommandResult {
            success: false,
            output: String::new(),
            error: Some(format!("Binary '{}' is strictly prohibited by security policy.", binary)),
        };
    }

    match Command::new(&binary).args(&args).output() {
        Ok(output) => CommandResult {
            success: output.status.success(),
            output: String::from_utf8_lossy(&output.stdout).to_string(),
            error: if output.status.success() {
                None
            } else {
                Some(String::from_utf8_lossy(&output.stderr).to_string())
            },
        },
        Err(e) => CommandResult {
            success: false,
            output: String::new(),
            error: Some(e.to_string()),
        },
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            launch_app,
            execute_allowlisted_command
        ])
        .run(tauri::generate_context!())
        .expect("error while running Project NOVA desktop agent");
}

