package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strconv"

	vosk "github.com/alphacep/vosk-api/go"
	uiprogress "github.com/gosuri/uiprogress"
	"github.com/joho/godotenv"
)

func main() {
    err := godotenv.Load()
    if err != nil {
        fmt.Println("Error loading .env file")
        return
    }

    frameSize := os.Getenv("FRAME_SIZE")

    // use ffmpeg to split audio into chunks of 1000 frames
    cmd := exec.Command("ffmpeg", "-loglevel", "quiet", "-i", "audio.wav", "-f", "segment",
        "-segment_time", frameSize, "-c", "copy", "audio-%09d.wav")

    err = cmd.Run()
    if err != nil {
        fmt.Println("Error executing command:", err)
        return
    }
    fmt.Println("audio.wav into chunked.")

    // get list of audio files
    files, err := filepath.Glob("audio-*.wav")
    if err != nil {
        fmt.Println("Error getting file list:", err)
        return
    }

    // sort the files by name
    sort.Strings(files)

    // create Vosk recognizer
    model, err := vosk.NewModel("model")
	if err != nil {
        fmt.Println("Error creating model:", err)
		return
	} else {
        fmt.Println("Created model")
    }

    // create a channel to receive the transcription results
    results := make([]chan []map[string]interface{}, 0)

    // process each audio file in a separate goroutine
    uiprogress.Start()

    // collect the results with goroutines and wait for them to finish
    for i, file := range files {
        r := make(chan []map[string]interface{})
        results = append(results, r)
        go func(i int, file string) {
            segments := collectSegments(file, model)
            r <- segments
            close(r)
        }(i, file)
    }

    allSegments := make([]map[string]interface{}, 0)
    for _, r := range results {
        segments := <-r
        allSegments = append(allSegments, segments...)
    }

    // write the results to a file
    f, err := os.Create("transcription.json")
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer f.Close()
    enc := json.NewEncoder(f)
    enc.SetIndent("", "  ")
    err = enc.Encode(allSegments)
    if err != nil {
        fmt.Println("Error writing file:", err)
        return
    }
    fmt.Println("Wrote transcription to transcription.json")


}

func collectSegments(file string, model *vosk.VoskModel) []map[string]interface{} {
	rec, err := vosk.NewRecognizer(model, 16000)
    if err != nil {
        fmt.Println("Error creating recognizer:", err)
        return nil
    }
	rec.SetWords(1)

    f, err := os.Open(file)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return nil
    }
    defer f.Close()
    stat, err := f.Stat()
    size := stat.Size()

    // read file in 1000 frame chunks
    frameSize,  _ := strconv.Atoi(os.Getenv("FRAME_SIZE"))
    chunkSize := frameSize * 2
    numChunks := int(size) / chunkSize

    bar := uiprogress.AddBar(numChunks).AppendCompleted().PrependElapsed()

    // create a slice to hold the results
    segments := make([]map[string]interface{}, 0)
    for i := 0; i < numChunks; i++ {
        // read chunk
        buf := make([]byte, chunkSize)
        _, err := f.Read(buf)
        if err != nil {
            fmt.Println("Error reading file:", err)
            return nil
        }

        // process chunk
        if rec.AcceptWaveform(buf) != 0 {
            result := rec.Result()
            var data map[string]interface{}
            err := json.Unmarshal([]byte(result), &data)
            if err != nil {
                fmt.Println("Error unmarshalling result:", err)
                return nil
            }
            segments = append(segments, data)
        }
        bar.Incr()
    }

    // process the final chunk
    finalResult := rec.FinalResult()
    var data map[string]interface{}
    err = json.Unmarshal([]byte(finalResult), &data)
    if err != nil {
        fmt.Println("Error unmarshalling final result:", err)
        return nil
    }
    segments = append(segments, data)

    // return segments
    return segments
}
