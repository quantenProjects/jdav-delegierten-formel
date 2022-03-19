// CC-0
use color_eyre::eyre::Result;
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
struct Record {
    #[serde(rename = "Sektion")]
    departement: String,
    #[serde(rename = "LV")]
    state_association: String,
    #[serde(rename = "M")]
    members: u32,
    #[serde(rename = "JL")]
    youth_leaders: u32,
}

#[derive(Debug, Serialize)]
struct OutputRecord {
    #[serde(rename = "Sektion")]
    departement: String,
    #[serde(rename = "LV")]
    state_association: String,
    #[serde(rename = "M")]
    members: u32,
    #[serde(rename = "JL")]
    youth_leaders: u32,
    div_jl: f64,
    div_members: f64,
    d_n: u32,
}

fn main() -> Result<()> {
    // init logging
    tracing_subscriber::fmt::init();

    // extract total number of delegates from command-line arg 1
    // (reminder: 0 is application name)
    let args: Vec<String> = std::env::args().collect();
    // number of total delegates
    let d = args[1].parse::<usize>()?;

    let mut rdr = csv::Reader::from_reader(std::io::stdin());
    let results: Result<Vec<Record>, _> = rdr.deserialize().collect();
    let results = results?;

    // number of DAV departements
    let k = results.len();
    // the difference to d is all we are interested in;
    let diff_d_k = (d - k) as u32;
    tracing::debug!("d = {}, k = {}, d-k = {}", d, k, d - k);

    // number of youth leaders in JDAV (JL_gesamt)
    let jl_total: u32 = results.iter().map(|record| record.youth_leaders).sum();
    tracing::debug!("JL_gesamt = {}", jl_total);

    // Σ_i=1^k √M_i
    let sum_of_rooted_members: f64 = results
        .iter()
        .map(|record| (record.members as f64).sqrt())
        .sum();
    tracing::debug!("Σ_i=1^k √M_i = {}", sum_of_rooted_members);

    let output_records: Vec<OutputRecord> = results
        .into_iter()
        .map(|record| {
            let div_jl = 0.5 * (record.youth_leaders as f64) / (jl_total as f64);
            let div_members = 0.5 * (record.members as f64).sqrt() / sum_of_rooted_members;
            let d_n = (1.0 + (diff_d_k as f64) * (div_jl + div_members)).round() as u32;
            OutputRecord {
                departement: record.departement,
                state_association: record.state_association,
                members: record.members,
                youth_leaders: record.youth_leaders,
                div_jl,
                div_members,
                d_n,
            }
        })
        .collect();

    let mut wtr = csv::Writer::from_writer(std::io::stdout());
    for record in output_records {
        wtr.serialize(record)?;
    }

    Ok(())
}
