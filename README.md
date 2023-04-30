# Hash Function Collision Handling Comparison

This repository contains an implementation of a project that compares the
performance of two different collision handling strategies for hash functions.
The project was created as a class assignment to apply and verify concepts
related to the manipulation of different data structures.

## Objective

The objective of this project is to compare the behavior of a hash function
implemented using two different collision handling strategies:

1. Collision handling using chaining
1. Collision handling using open addressing

The performance of these strategies will be compared using a poorly designed
hash function and a more refined one that results in fewer collisions.

## Implementation Details

- You may choose the programming language for the implementation.
- The choice of the hash function is up to the team. The input data will only be
  non-repeating integers.
- The implementation approach should be consistent for both collision handling
  methods.
- Input data for the construction of the hash tables should be based on the
  provided text files in the following format: `ConstruirN.txt`.
  - [Dataset 5](https://drive.google.com/file/d/1EmpAXby4IhxmQlQrdmC2HGwO1_4ao5XZ/view?usp=sharing)
- The values to be used for queries are available in the same link in the format
  `ConsultarN.txt`.

## Evaluation Criteria

The performance of the methods should be evaluated based on the following
criteria:

1. During the construction of the structures (insertion of elements in the
   table):

   - Chronological time spent on building both structures
   - Number of key comparisons made to build each structure (excluding the test
     to check if the position is occupied or not)

1. During the query stage:

   - Chronological time spent on querying all elements in the file within the
     two previously constructed tables
   - Number of key comparisons made to query all elements from the query files
     in the previously formed structures (excluding the test to check if the
     position is occupied or not)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
