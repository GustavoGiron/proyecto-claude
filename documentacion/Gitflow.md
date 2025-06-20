
## 🛠️ Instrucciones para el flujo de trabajo Git

A continuación, se detalla el flujo de trabajo a seguir utilizando **Git Flow** en conjunto con buenas prácticas de desarrollo. Este proceso aplica tanto para nuevas funcionalidades, correcciones como lanzamientos oficiales.

### 🔁 Iniciar una feature
```bash
git flow feature start nombre
```

### 💻 Trabajar y hacer commits
Pueden realizar este paso desde **GitKraken**, o bien usar la terminal:

```bash
git add .
git commit -m "Descripción del cambio"
```

📌 **Importante:** Todos los commits deberán seguir el estándar de [Conventional Commits](https://www.conventionalcommits.org/), asegurando claridad y trazabilidad en cada cambio realizado, es importante que el commit sea relacionado a lo que hicieron, por que la ingeneria revisa eso (esto me lo contaron y pues mejor prevenir que lamentar.)

### ✅ Finalizar una feature
```bash
git flow feature finish nombre
git push origin develop
```

---

### 🚀 Iniciar un release
```bash
git flow release start v1.1.0
```

### 📦 Finalizar un release
```bash
git flow release finish v1.1.0
git push origin main develop
git push --tags
```

---

### 🐞 Iniciar un hotfix
```bash
git flow hotfix start v1.1.1
```

### ✔️ Finalizar un hotfix
```bash
git flow hotfix finish v1.1.1
git push origin main develop
git push --tags
```

---

## 📂 Nomenclatura de ramas

Para mantener orden y claridad en el repositorio, seguiremos esta estructura para las ramas:

```
feature/carnet/funcionalidad
```

Por ejemplo:
- `feature/carnet/fun1`
- `feature/carnet/fun2`

📌 No eliminar las ramas ya usadas.

---

## 📄 Documentación

El auxiliar nos indicó crear una carpeta por persona, aunque aún no se ha definido cómo se organizará esto exactamente. Lo discutiremos más adelante para tener un criterio claro entre todos.

---

## 🗂️ Manejo de tareas

Usaremos **Kanban** para gestionar las tareas del proyecto. Cada integrante tendrá su propio tablero donde irá moviendo sus tareas a medida que avanzan.

---

## 📘 Integración de Swagger

Además, debemos implementar lo siguiente:  
👉 [Automatically Generating Swagger Specifications](https://swagger.io/blog/api-development/automatically-generating-swagger-specifications-wi/)

Este artículo propone una forma automatizada de generar especificaciones OpenAPI (Swagger) durante el desarrollo. A mí me pareció muy útil porque permite visualizar y probar los endpoints directamente desde la interfaz de Swagger, sin necesidad de usar Postman constantemente.

📄 Esto facilita la documentación en tiempo real, mejora la comunicación entre equipos y asegura consistencia en el diseño de APIs.

Vamos a revisarlo e integrarlo pronto en el flujo de desarrollo.

---

Si tienen dudas o algo no queda claro, coordinamos una breve reunión para alinear criterios. La idea es que todos avancemos alineados y con buenas prácticas.
