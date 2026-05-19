def escapar_llaves(texto: str) -> str:
    """Escapa llaves literales en texto externo para que no rompan str.format()."""
    return texto.replace("{", "{{").replace("}", "}}")
