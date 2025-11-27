package main

import (
	"fmt"
	"log"
	"net/http"
	"github.com/glebarez/go-sqlite"
)

func handler(w http.ResponseWriter, r *http.Request){

	fmt.Fprintf(w," Test one %s", r.URL.Path[1:])
}

func main() {

	db, err := sql.Open("sqlite","

	http.HandleFunc("/",handler)
	log.Fatal(http.ListenAndServe(":8080",nil))
}
