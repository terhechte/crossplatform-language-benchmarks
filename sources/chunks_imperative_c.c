#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

// We're using uint64_t as `usize` and `Int` in Rust / Swift also have 8byte

uint64_t* resize_image(uint64_t* image, uint64_t size, uint64_t width, uint64_t scale, uint64_t* rsize) {
    uint64_t *result = malloc(sizeof(uint64_t) * (size / scale));
    uint64_t pos = 0;
    for (uint64_t i=0; i<size; i+=width) {
        for (uint64_t i2=i; i2<(i + width); i2+=scale) {
            uint64_t sum = 0;
            for (uint64_t i3=i2; i3<(i2 + scale); i3+=1) {
                sum += image[i3];
            }
            result[pos++] = sum;
        }
    }
    *rsize = pos;
    return result;
}

uint64_t* generate(uint64_t* size) {
    const uint64_t count = 1000000;
    uint64_t image[] = {
        1, 0, 0, 4, 4, 0, 0, 1,
        0, 0, 0, 9, 9, 0, 0, 0,
        0, 0, 0, 9, 9, 0, 0, 0,
        4, 9, 9, 9, 9, 9, 9, 4,
        4, 9, 9, 9, 9, 9, 9, 4,
        0, 0, 0, 9, 9, 0, 0, 0,
        0, 0, 0, 9, 9, 0, 0, 0,
        1, 0, 0, 4, 4, 0, 0, 1,
    };
    uint64_t* array = malloc(count * sizeof(image));
    uint64_t pos = 0;
    for (uint64_t i=0; i<count; i++) {
      for (uint64_t i=0; i<sizeof(image)/sizeof(int64_t); i+=1) {
            array[pos++] = image[i];
        }
    }
    *size = (count * sizeof(image)) / sizeof(uint64_t);
    return array;
}

int main(int argc, const char * argv[]) {
    uint64_t image_size = 0;
    uint64_t* image = generate(&image_size);

    uint64_t result1_size, result2_size, result3_size;
    uint64_t *result1 = resize_image(image, image_size, 8, 2, &result1_size);
    uint64_t *result2 = resize_image(image, image_size, 32, 8, &result2_size);
    uint64_t *result3 = resize_image(image, image_size, 16, 4, &result3_size);

    uint64_t fr1 = 0;
    for (uint64_t s = 0; s < result1_size; s++) {
      fr1 += result1[s];
    }

    uint64_t fr2 = 0;
    for (uint64_t s = 0; s < result2_size; s++) {
      fr2 += result2[s];
    }

    uint64_t fr3 = 0;
    for (uint64_t s = 0; s < result3_size; s++) {
      fr3 += result3[s];
    }

    free(result1);
    free(result2);
    free(result3);

    printf("sum: %lli\n", fr1);
    printf("%lli %lli %lli\n", result1_size, result2_size, result3_size);
    printf("%lli %lli %lli\n", fr1 / result1_size, fr2 / result2_size, fr3 / result3_size);

    free(image);
    return 0;
}
