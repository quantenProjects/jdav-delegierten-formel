# jdav-calc-rust

Eine weitere Implementierung der Delegiertenberechnung in Rust.

Diese wurde netterweise von einem Freund auf Basis der BJO geschrieben.

## Benutzung

Erwartet ein Kommandozeilenargument: `D` (also z.B. `jdav-calc 10`).
Liest vom stdin, schreibt in stdout.

Wenn Du noch die Zwischensummen von JL und die Summe der gewurzelten Mitglieder haben willst, kannst Du `RUST_LOG=debug` setzen.

```bash
cat test_sektionen.csv | RUST_LOG=debug jdav-calc 10
```

Dann ist der Output aber erst nach 3 Zeilen verwertbares CSV. 
