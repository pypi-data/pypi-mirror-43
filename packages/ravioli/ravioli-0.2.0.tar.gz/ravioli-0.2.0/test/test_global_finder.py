from ravioli.global_finder import find_globals


# Extract a list of names from the list of result objects.
def extract_names(results):
    return [result.name for result in results]


def test_a_single_global():
    code = """
            int a_global;
            """
    results = find_globals(code)
    assert ('a_global' in extract_names(results))


def test_multiple_globals():
    code = """
            int a_global;
            uint8_t another_global;
            """
    results = find_globals(code)
    assert ('a_global' in extract_names(results))
    assert ('another_global' in extract_names(results))


def test_a_global_with_assignment():
    code = """
            int a_global=0;
            """
    results = find_globals(code)
    assert ('a_global' in extract_names(results))


def test_with_assignment_and_whitespace():
    code = """
            int a_global = 0;
            """
    results = find_globals(code)
    assert ('a_global' in extract_names(results))


def test_a_function_variable_is_not_found():
    code = """
            void a_function() {
                int not_a_global;
            }
            """
    results = find_globals(code)
    assert ('not_a_global' not in extract_names(results))


def test_a_deeper_function_variable_is_not_found():
    code = """
            void a_function(int x) {
                if (x > 0) {
                    // do something
                }
                else {
                    int not_a_global;
                }
            }
            """
    results = find_globals(code)
    assert ('not_a_global' not in extract_names(results))


def test_a_static_is_not_global():
    code = """
            int a_global;
            static int not_a_global;
            """
    results = find_globals(code)
    assert ('not_a_global' not in extract_names(results))


def test_typedefs():
    code = """
            typedef int my_new_type;
            my_new_type a_global;
            """
    results = find_globals(code)
    assert(len(results) == 1)
    assert('a_global' in extract_names(results))


def test_structs():
    code = """
            struct point_t {
                int x;
                int y;
            };
            struct point_t a_global;
            """
    results = find_globals(code)
    assert(len(results) == 1)
    assert('a_global' in extract_names(results))


def test_struct_globals_declared_with_definition():
    code = """
            struct point_t {
                int x;
                int y;
            } a_global;
            """
    results = find_globals(code)
    assert(len(results) == 1)
    assert('a_global' in extract_names(results))


def test_an_extern_is_not_global():
    code = """
            int a_global;
            extern int not_a_global;
            """
    results = find_globals(code)
    assert ('not_a_global' not in extract_names(results))


def test_commented_global_is_not_global():
    code = """
            int a_global;
            /*int not_a_global;*/
            """
    results = find_globals(code)
    assert ('not_a_global' not in extract_names(results))


def test_global_in_single_line_comment_not_counted():
    code = """
            int a_global;
            //int not_a_global;
            """
    results = find_globals(code)
    assert ('not_a_global' not in extract_names(results))


def test_dont_count_preprocessor_ifs():
    code = """
            #if configUSE_PREEMPTION == 0
            {
                taskYIELD();
            }
            #endif
            """
    results = find_globals(code)
    assert ('configUSE_PREEMPTION' not in extract_names(results))


def test_dont_count_preprocessor_elifs():
    code = """
            #elif configUSE_PREEMPTION == 0
            {
                taskYIELD();
            }
            #endif
            """
    results = find_globals(code)
    assert ('configUSE_PREEMPTION' not in extract_names(results))


def test_a_name_containing_extern_is_global():
    code = """
            int external_global;
            """
    results = find_globals(code)
    assert ('external_global' in extract_names(results))


def test_a_name_containing_static_is_global():
    code = """
            int static_constant;
            """
    results = find_globals(code)
    assert ('static_constant' in extract_names(results))


def test_a_global_array():
    code = """
            char global_str[] = "abc";
            """
    results = find_globals(code)
    assert ('global_str' in extract_names(results))


def test_a_global_sized_array():
    code = """
            char global_array[10];
            """
    results = find_globals(code)
    assert ('global_array' in extract_names(results))


def test_a_global_sized_array_with_assignment():
    code = """
            int global_array[3] = [1, 2, 3];
            """
    results = find_globals(code)
    assert ('global_array' in extract_names(results))


def test_dont_count_const_globals():
    # They really don't add to the complexity.
    code = """
            const char global_str[] = "abc";
            """
    results = find_globals(code)
    assert ('global_str' not in extract_names(results))


# Find line numbers of globals.
def test_a_line_number_is_found():
    code = """int a_global;
            """
    results = find_globals(code)
    assert ('a_global' in extract_names(results))
    assert (1 == results[0].line_number)


def test_another_line_number_is_found():
    code = """int a_global;
            int another_global;
            """
    results = find_globals(code)
    assert (1 == results[0].line_number)
    assert (2 == results[1].line_number)


def test_a_line_number_with_a_comment():
    code = """// This is a comment.
            int a_global;
            int another_global;
            """
    results = find_globals(code)
    assert (2 == results[0].line_number)
    assert (3 == results[1].line_number)


def test_a_line_number_with_a_blank_line():
    code = """
            int a_global;
            int another_global;
            """
    results = find_globals(code)
    assert (2 == results[0].line_number)
    assert (3 == results[1].line_number)


def test_line_number_with_a_declaration_as_part_of_a_definition():
    code = """struct point_t {
                int x;
                int y;
            } a_global;
            """
    results = find_globals(code)
    assert (4 == results[0].line_number)

