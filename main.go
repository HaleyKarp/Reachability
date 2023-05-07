package main

import (
	"fmt"
	"reachability_sandbox/local_imports"
)

func main() {
	x := 5
	fmt.Println("The double of", x, "is", local_imports.double(x))
}
