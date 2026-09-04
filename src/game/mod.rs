//! Everything about the game installation. Knows nothing about CDP or patching.

pub mod locate;
pub mod process;

use std::path::PathBuf;

/// A located game installation. This struct is everything we know about the game.
#[derive(Debug, Clone)]
pub struct Install {
    pub dir: PathBuf,
    pub exe: PathBuf,
    /// `version` from resources/app/package.json
    pub version: String,
}
