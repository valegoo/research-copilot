import os

# Script para generar el guion y que el usuario lo copie
guion = """
========================================================================
       GUION DE PRESENTACIÓN - RESEARCH COPILOT (PUCP)
========================================================================
ESTUDIANTE: Valeria Gonzales Torres
CURSO: Prompt Engineering: Aplicaciones de IA Avanzadas
TEMA: Neoliberalismo y Educación Superior
------------------------------------------------------------------------

PARTE 1: INTRODUCCIÓN (0:00 - 0:30)
------------------------------------------------------------------------
Voz: "Hola, mi nombre es Valeria Gonzales Torres, estudiante de la PUCP. 
Hoy les presento Research Copilot, una plataforma de inteligencia 
académica diseñada para acelerar la revisión de literatura."

Visual: [Mostrar la página principal de la app - Diseño Pastel]

Voz: "Mi colección consta de 21 artículos académicos especializados en 
el Neoliberalismo y su impacto en la Educación Superior. El problema 
que resolvemos es la saturación de información: en lugar de leer miles 
de páginas, Research Copilot permite 'dialogar' con los autores con 
total rigor científico y fuentes verificables."

PARTE 2: ARQUITECTURA DEL SISTEMA (0:30 - 1:00)
------------------------------------------------------------------------
Visual: [Mostrar el diagrama de arquitectura del README]

Voz: "Técnicamente, el sistema es un pipeline de RAG (Generación 
Aumentada por Recuperación). Los documentos pasan por un proceso de 
ingesta con PyMuPDF, se dividen en fragmentos semánticos y se 
almacenan como vectores en ChromaDB. Utilizamos los modelos 
text-embedding-3-small y GPT-4o de OpenAI para garantizar respuestas 
precisas."

PARTE 3: DEMO EN VIVO (1:00 - 2:15)
------------------------------------------------------------------------
Visual: [Pestaña de Chat en vivo]

Voz: "Veamos el sistema en acción. Primero, una pregunta directa: 
'¿Cómo define David Harvey el neoliberalismo?'"
[Mostrar respuesta rápida]

Voz: "Ahora, una más compleja que requiere cruzar información: 
'¿Qué puntos en común tienen Saura y Alvesson sobre la productividad?'"
[Mostrar cómo cita a ambos autores]

Voz: "Y finalmente, para evitar alucinaciones: '¿Qué dicen los textos 
sobre Islandia?'. El sistema reconoce correctamente que no tiene 
esa información."

Visual: [Mostrar Paper Browser y Analytics]
Voz: "Como ven, cada respuesta incluye citas en formato APA y analytics 
en tiempo real."

PARTE 4: DISCUSIÓN TÉCNICA (2:15 - 3:00)
------------------------------------------------------------------------
Visual: [Tabla de estrategias de prompts en el README]

Voz: "Implementamos 4 estrategias de prompting. Desde la v1 básica 
hasta la v4 de Chain-of-Thought para análisis profundos. Usamos 
segmentos de 512 tokens para un balance perfecto entre precisión 
y contexto."

PARTE 5: CONCLUSIONES (3:00 - 3:30)
------------------------------------------------------------------------
Voz: "Aprendí a integrar bases vectoriales para eliminar alucinaciones. 
Como limitaciones: el sistema no lee tablas complejas o imágenes. 
A futuro, planeo implementar Reranking y soporte multi-modal. 
¡Muchas gracias!"

========================================================================
"""

with open("GUION_PRESENTACION_VALERIA.txt", "w", encoding="utf-8") as f:
    f.write(guion)

print("¡Listo! El guion ha sido guardado como GUION_PRESENTACION_VALERIA.txt")
