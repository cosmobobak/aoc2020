

fn main() {
    let text = include_str!("../task1.txt");
    let lines = text.lines();
    let nums = lines.map(|s| s.parse::<i32>().unwrap()).collect::<Vec<_>>();
    
    let (a, b) = nums.iter()
        .flat_map(|n| nums.iter().map(move |&m| (*n, m)))
        .find(|(n, m)| n + m == 2020)
        .unwrap();

    println!("{}", a * b);

    let (a, b, c) = nums.iter()
        .flat_map(|n| nums.iter().map(move |&m| (*n, m)))
        .flat_map(|(n, m)| nums.iter().map(move |&l| (n, m, l)))
        .find(|(n, m, l)| n + m + l == 2020)
        .unwrap();

    println!("{}", a * b * c);
}
