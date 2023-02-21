vosk_path=$(pwd)/vosk-linux-x86_64-0.3.45
shared=$vosk_path
cpp_flags="-I $vosk_path"
ld_flags="-L $vosk_path"

LD_LIBRARY_PATH=$vosk_path CGO_CPPFLAGS=$cpp_flags CGO_LDFLAGS=$ld_flags go run .
