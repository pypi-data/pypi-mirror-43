#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "../src/c/detools.h"

#define MIN(a, b) ((a) < (b) ? (a) : (b))

struct io_t {
    FILE *ffrom_p;
    struct {
        uint8_t *actual_p;
        uint8_t *expected_p;
        size_t size;
        size_t written;
    } to;
};

static void *mymalloc(size_t size)
{
    void *buf_p;

    buf_p = malloc(size);
    assert(buf_p != NULL);

    return (buf_p);
}

static FILE *myfopen(const char *name_p, const char *flags_p)
{
    FILE *file_p;

    file_p = fopen(name_p, flags_p);
    assert(file_p != NULL);

    return (file_p);
}

static void io_init(struct io_t *self_p,
                    const char *from_p,
                    const char *to_p)
{
    FILE *file_p;
    long size;

    self_p->ffrom_p = myfopen(from_p, "rb");

    file_p = myfopen(to_p, "rb");

    assert(fseek(file_p, 0, SEEK_END) == 0);
    size = ftell(file_p);
    assert(size > 0);
    self_p->to.size = (size_t)size;
    assert(fseek(file_p, 0, SEEK_SET) == 0);

    self_p->to.actual_p = mymalloc(self_p->to.size);
    self_p->to.expected_p = mymalloc(self_p->to.size);
    assert(fread(self_p->to.expected_p, self_p->to.size, 1, file_p) == 1);

    fclose(file_p);

    self_p->to.written = 0;
}

static void io_assert_to_ok(struct io_t *self_p)
{
    assert(self_p->to.written == self_p->to.size);
    assert(memcmp(self_p->to.actual_p,
                  self_p->to.expected_p,
                  self_p->to.size) == 0);
}

static int io_read(void *arg_p, uint8_t *buf_p, size_t size)
{
    struct io_t *self_p;

    self_p = (struct io_t *)arg_p;

    if (fread(buf_p, size, 1, self_p->ffrom_p) == 1) {
        return (0);
    } else {
        return (-1);
    }
}

static int io_seek(void *arg_p, int offset)
{
    struct io_t *self_p;

    self_p = (struct io_t *)arg_p;

    return (fseek(self_p->ffrom_p, offset, SEEK_CUR));
}

static int io_write(void *arg_p, const uint8_t *buf_p, size_t size)
{
    struct io_t *self_p;

    self_p = (struct io_t *)arg_p;

    assert(self_p->to.size - self_p->to.written >= size);

    memcpy(&self_p->to.actual_p[self_p->to.written], buf_p, size);
    self_p->to.written += size;

    return (0);
}

static uint8_t *read_init(const char *name_p, size_t *size_p)
{
    FILE *file_p;
    void *buf_p;
    long size;

    file_p = myfopen(name_p, "rb");

    assert(fseek(file_p, 0, SEEK_END) == 0);
    size = ftell(file_p);
    assert(size > 0);
    *size_p = (size_t)size;
    assert(fseek(file_p, 0, SEEK_SET) == 0);

    buf_p = mymalloc(*size_p);
    assert(fread(buf_p, *size_p, 1, file_p) == 1);

    fclose(file_p);

    return (buf_p);
}

static uint8_t *patch_init(const char *patch_p, size_t *patch_size_p)
{
    return (read_init(patch_p, patch_size_p));
}

static void assert_apply_patch(const char *from_p,
                               const char *patch_p,
                               const char *to_p)
{
    int res;
    const char *actual_to_p = "assert-apply-patch.new";
    FILE *actual_fto_p;
    FILE *expected_fto_p;
    int actual_byte;
    int expected_byte;

    res = detools_apply_patch_filenames(from_p,
                                        patch_p,
                                        actual_to_p);

    if (res != 0) {
        printf("FAIL: apply of '%s' to '%s' to '%s' failed with '%s' (%d)\n",
               patch_p,
               from_p,
               to_p,
               detools_error_as_string(-res),
               res);
        exit(1);
    }

    actual_fto_p = myfopen(actual_to_p, "rb");
    expected_fto_p = myfopen(to_p, "rb");

    do {
        actual_byte = getc(actual_fto_p);
        expected_byte = getc(expected_fto_p);
        assert(actual_byte == expected_byte);
    } while (actual_byte != EOF);
}

static void assert_apply_patch_error(const char *from_p,
                                     const char *patch_p,
                                     int expected_res)
{
    const char *actual_to_p = "assert-apply-patch.new";
    int res;

    res = detools_apply_patch_filenames(from_p,
                                        patch_p,
                                        actual_to_p);

    if (res != expected_res) {
        printf("FAIL: res: %d, expected_res: %d\n", res, expected_res);
        exit(1);
    }
}

static void test_apply_patch_foo(void)
{
    assert_apply_patch("tests/files/foo.old",
                       "tests/files/foo.patch",
                       "tests/files/foo.new");
}

static void test_apply_patch_foo_backwards(void)
{
    assert_apply_patch("tests/files/foo.new",
                       "tests/files/foo-backwards.patch",
                       "tests/files/foo.old");
}

static void test_apply_patch_micropython(void)
{
    assert_apply_patch(
        "tests/files/micropython-esp8266-20180511-v1.9.4.bin",
        "tests/files/micropython-esp8266-20180511-v1.9.4--20190125-v1.10.patch",
        "tests/files/micropython-esp8266-20190125-v1.10.bin");
}

static void test_apply_patch_foo_none_compression(void)
{
    assert_apply_patch("tests/files/foo.old",
                       "tests/files/foo-none.patch",
                       "tests/files/foo.new");
}

static void test_apply_patch_micropython_none_compression(void)
{
    assert_apply_patch(
        "tests/files/micropython-esp8266-20180511-v1.9.4.bin",
        "tests/files/micropython-esp8266-20180511-v1.9.4--20190125-v1.10-none.patch",
        "tests/files/micropython-esp8266-20190125-v1.10.bin");
}

static void test_apply_patch_foo_crle_compression(void)
{
    assert_apply_patch("tests/files/foo.old",
                       "tests/files/foo-crle.patch",
                       "tests/files/foo.new");
}

static void test_apply_patch_micropython_crle_compression(void)
{
    assert_apply_patch(
        "tests/files/micropython-esp8266-20180511-v1.9.4.bin",
        "tests/files/micropython-esp8266-20180511-v1.9.4--20190125-v1.10-crle.patch",
        "tests/files/micropython-esp8266-20190125-v1.10.bin");
}

static void test_apply_patch_micropython_in_place(void)
{
    assert_apply_patch_error(
        "tests/files/micropython-esp8266-20180511-v1.9.4.bin",
        "tests/files/micropython-esp8266-20180511-v1.9.4--"
        "20190125-v1.10-in-place.patch",
        -DETOOLS_NOT_IMPLEMENTED);
}

static void test_apply_patch_foo_in_place_3000_1500(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-in-place-3000-1500.patch",
                             -DETOOLS_NOT_IMPLEMENTED);
}

static void test_apply_patch_foo_in_place_3k_1_5k(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-in-place-3k-1.5k.patch",
                             -DETOOLS_NOT_IMPLEMENTED);
}

static void test_apply_patch_foo_in_place_3000_1500_1500(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-in-place-3000-1500-1500.patch",
                             -DETOOLS_NOT_IMPLEMENTED);
}

static void test_apply_patch_foo_in_place_3000_500(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-in-place-3000-500.patch",
                             -DETOOLS_NOT_IMPLEMENTED);
}

static void test_apply_patch_foo_in_place_3000_500_crle(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-in-place-3000-500-crle.patch",
                             -DETOOLS_NOT_IMPLEMENTED);
}

static void test_apply_patch_foo_in_place_6000_1000_crle(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-in-place-6000-1000-crle.patch",
                             -DETOOLS_NOT_IMPLEMENTED);
}

static void test_apply_patch_bsdiff(void)
{
    assert_apply_patch("tests/files/bsdiff.py",
                       "tests/files/bsdiff-READ-ME.patch",
                       "tests/files/READ-ME.rst");
}

static void test_apply_patch_sais(void)
{
    assert_apply_patch("tests/files/sais.c",
                       "tests/files/sais-READ-ME.patch",
                       "tests/files/READ-ME.rst");
}

static void test_apply_patch_3f5531ba56182a807a5c358f04678b3b026d3a(void)
{
    assert_apply_patch(
        "tests/files/3f5531ba56182a807a5c358f04678b3b026d3a.bin",
        "tests/files/3f5531ba56182a807a5c358f04678b3b026d3a-READ-ME.patch",
        "tests/files/READ-ME.rst");
}

static void test_apply_patch_b2db59ab76ca36f67e61f720857021df8a660b(void)
{
    assert_apply_patch(
        "tests/files/b2db59ab76ca36f67e61f720857021df8a660b.bin",
        "tests/files/b2db59ab76ca36f67e61f720857021df8a660b-READ-ME.patch",
        "tests/files/READ-ME.rst");
}

static void test_apply_patch_d027a1e1f752f15b6a13d9f9d775f3914c83f7(void)
{
    assert_apply_patch(
        "tests/files/d027a1e1f752f15b6a13d9f9d775f3914c83f7.bin",
        "tests/files/d027a1e1f752f15b6a13d9f9d775f3914c83f7-READ-ME.patch",
        "tests/files/READ-ME.rst");
}

static void test_apply_patch_eb9ed88e9975028c4694e070cfaece2498e92d(void)
{
    assert_apply_patch(
        "tests/files/eb9ed88e9975028c4694e070cfaece2498e92d.bin",
        "tests/files/eb9ed88e9975028c4694e070cfaece2498e92d-READ-ME.patch",
        "tests/files/READ-ME.rst");
}

static void test_apply_patch_no_delta(void)
{
    assert_apply_patch("tests/files/foo.new",
                       "tests/files/foo-no-delta.patch",
                       "tests/files/foo.new");
}

static void test_apply_patch_empty(void)
{
    assert_apply_patch("tests/files/empty.old",
                       "tests/files/empty.patch",
                       "tests/files/empty.new");
}

static void test_apply_patch_empty_none_compression(void)
{
    assert_apply_patch("tests/files/empty.old",
                       "tests/files/empty-none.patch",
                       "tests/files/empty.new");
}

static void test_apply_patch_empty_crle_compression(void)
{
    assert_apply_patch("tests/files/empty.old",
                       "tests/files/empty.patch",
                       "tests/files/empty.new");
}

static void test_apply_patch_foo_short(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-short.patch",
                             -DETOOLS_CORRUPT_PATCH);
}

static void test_apply_patch_foo_short_none_compression(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-short-none.patch",
                             -DETOOLS_CORRUPT_PATCH);
}

static void test_apply_patch_foo_long(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-bad-lzma-end.patch",
                             -DETOOLS_LZMA_DECODE);
}

static void test_apply_patch_foo_diff_data_too_long(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-diff-data-too-long.patch",
                             -DETOOLS_CORRUPT_PATCH);
}

static void test_apply_patch_foo_extra_data_too_long(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-extra-data-too-long.patch",
                             -DETOOLS_CORRUPT_PATCH);
}

static void test_apply_patch_foo_bad_patch_type(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-bad-patch-type.patch",
                             -DETOOLS_BAD_PATCH_TYPE);
}

static void test_apply_patch_foo_bad_compression(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-bad-compression.patch",
                             -DETOOLS_BAD_COMPRESSION);
}

static void test_apply_patch_one_byte(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-one-byte.patch",
                             -DETOOLS_SHORT_HEADER);
}

static void test_apply_patch_short_to_size(void)
{
    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-short-to-size.patch",
                             -DETOOLS_SHORT_HEADER);
}

static void test_apply_patch_file_open_error(void)
{
    assert_apply_patch_error("tests/files/foo.old.missing",
                             "tests/files/foo-bad-compression.patch",
                             -DETOOLS_FILE_OPEN_FAILED);

    assert_apply_patch_error("tests/files/foo.old",
                             "tests/files/foo-bad-compression.patch.missing",
                             -DETOOLS_FILE_OPEN_FAILED);

    assert(detools_apply_patch_filenames("tests/files/foo.old",
                                         "tests/files/foo-bad-compression.patch",
                                         "") == -DETOOLS_FILE_OPEN_FAILED);
}

static void test_apply_patch_foo_compression_incremental(void)
{
    struct detools_apply_patch_t apply_patch;
    struct io_t io;
    const uint8_t *patch_p;
    size_t patch_size;
    size_t expected_patch_size;
    size_t patch_offset;
    int res;

    io_init(&io, "tests/files/foo.old", "tests/files/foo.new");
    patch_p = patch_init("tests/files/foo.patch", &patch_size);
    expected_patch_size = patch_size;

    assert(detools_apply_patch_init(&apply_patch,
                                    io_read,
                                    io_seek,
                                    patch_size,
                                    io_write,
                                    &io) == 0);

    /* Process up to 64 new patch bytes per iteration. */
    patch_offset = 0;

    while (patch_offset < expected_patch_size) {
        patch_size = MIN(expected_patch_size - patch_offset, 64);
        res = detools_apply_patch_process(&apply_patch,
                                          &patch_p[patch_offset],
                                          patch_size);
        assert(res == 0);
        patch_offset += patch_size;
    }

    assert(detools_apply_patch_finalize(&apply_patch) == 0);
    io_assert_to_ok(&io);
}

static void test_error_as_string(void)
{
    assert(strcmp(detools_error_as_string(DETOOLS_NOT_IMPLEMENTED),
                  "Function not implemented.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_NOT_DONE),
                  "Not done.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_BAD_PATCH_TYPE),
                  "Bad patch type.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_BAD_COMPRESSION),
                  "Bad compression.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_INTERNAL_ERROR),
                  "Internal error.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_LZMA_INIT),
                  "LZMA init.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_LZMA_DECODE),
                  "LZMA decode.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_OUT_OF_MEMORY),
                  "Out of memory.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_CORRUPT_PATCH),
                  "Corrupt patch.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_IO_FAILED),
                  "Input/output failed.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_ALREADY_DONE),
                  "Already done.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_FILE_OPEN_FAILED),
                  "File open failed.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_FILE_CLOSE_FAILED),
                  "File close failed.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_FILE_READ_FAILED),
                  "File read failed.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_FILE_WRITE_FAILED),
                  "File write failed.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_FILE_SEEK_FAILED),
                  "File seek failed.") == 0);
    assert(strcmp(detools_error_as_string(DETOOLS_FILE_TELL_FAILED),
                  "File tell failed.") == 0);
    assert(strcmp(detools_error_as_string(-1),
                  "Unknown error.") == 0);
}

int main()
{
    test_apply_patch_foo();
    test_apply_patch_foo_backwards();
    test_apply_patch_micropython();
    test_apply_patch_foo_none_compression();
    test_apply_patch_micropython_none_compression();
    test_apply_patch_foo_crle_compression();
    test_apply_patch_micropython_crle_compression();
    test_apply_patch_micropython_in_place();
    test_apply_patch_foo_in_place_3000_1500();
    test_apply_patch_foo_in_place_3k_1_5k();
    test_apply_patch_foo_in_place_3000_1500_1500();
    test_apply_patch_foo_in_place_3000_500();
    test_apply_patch_foo_in_place_3000_500_crle();
    test_apply_patch_foo_in_place_6000_1000_crle();
    test_apply_patch_bsdiff();
    test_apply_patch_sais();
    test_apply_patch_3f5531ba56182a807a5c358f04678b3b026d3a();
    test_apply_patch_b2db59ab76ca36f67e61f720857021df8a660b();
    test_apply_patch_d027a1e1f752f15b6a13d9f9d775f3914c83f7();
    test_apply_patch_eb9ed88e9975028c4694e070cfaece2498e92d();
    test_apply_patch_no_delta();
    test_apply_patch_empty();
    test_apply_patch_empty_none_compression();
    test_apply_patch_empty_crle_compression();

    test_apply_patch_empty();
    test_apply_patch_foo_short();
    test_apply_patch_foo_short_none_compression();
    test_apply_patch_foo_long();
    test_apply_patch_foo_diff_data_too_long();
    test_apply_patch_foo_extra_data_too_long();
    test_apply_patch_foo_bad_patch_type();
    test_apply_patch_foo_bad_compression();
    test_apply_patch_one_byte();
    test_apply_patch_short_to_size();
    test_apply_patch_file_open_error();

    test_apply_patch_foo_compression_incremental();

    test_error_as_string();

    return (0);
}
