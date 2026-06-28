from pathlib import Path

path = Path("builder.pyw")
text = path.read_text(encoding="utf-8")
text = text.replace("#00cccc", "#cc0000")
text = text.replace("#00ffff", "#ff0000")
text = text.replace("#009999", "#990000")
text = text.replace("fg_color=\"transparent\"", "fg_color=\"#000000\"")
text = text.replace("text=\"Opções do Construtor\"", "text=\"Opções de Stealer\"")
text = text.replace("text=\"Construtor\"", "text=\"Stealer\"")
path.write_text(text, encoding="utf-8")
print("builder theme updated")
