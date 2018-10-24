fn resize_image(image: &[usize], width: usize, scale: usize) -> Vec<usize> {
    image.chunks(width)
        .map(|slice| slice.chunks(scale).map(|chunk| { chunk.iter().sum::<usize>() }))
        .flatten()
        .collect()
}

fn generate() -> Vec<usize> {
    let image = [
        1, 0, 0, 4, 4, 0, 0, 1,
        0, 0, 0, 9, 9, 0, 0, 0,
        0, 0, 0, 9, 9, 0, 0, 0,
        4, 9, 9, 9, 9, 9, 9, 4,
        4, 9, 9, 9, 9, 9, 9, 4,
        0, 0, 0, 9, 9, 0, 0, 0,
        0, 0, 0, 9, 9, 0, 0, 0,
        1, 0, 0, 4, 4, 0, 0, 1,
    ];
    let nr = 1000000;
    let mut result: Vec<usize> = Vec::with_capacity(nr * image.len());
    for _ in 0..nr {
        result.extend_from_slice(&image);
    }
    result
}

fn main() {
    let image = generate();
    let result1 = resize_image(&image, 8, 2);
    let result2 = resize_image(&image, 32, 8);
    let result3 = resize_image(&image, 16, 4);

    let fr1 = result1.iter().sum::<usize>() / result1.len();
    let fr2 = result2.iter().sum::<usize>() / result2.len();
    let fr3 = result3.iter().sum::<usize>() / result3.len();

    println!("{}, {}, {}", result1.len(), result2.len(), result3.len());
    println!("{}, {}, {}", fr1, fr2, fr3);
}
