import { useState, useEffect } from "react";
import { getMateriaPrima, crearMateriaPrima, actualizarMateriaPrima, eliminarMateriaPrima } from "../../services/api";

const AdminMateriaPrima = () => {
  const [materiaPrima, setMateriaPrima] = useState([]); // Lista de materia prima
  const [nuevaMateria, setNuevaMateria] = useState({
    nombre: "",
    cantidad_disponible: "",
    precio_por_unidad: "",
    producto_id: "",
  });
  const [materiaSeleccionada, setMateriaSeleccionada] = useState(null); // Materia en edición
  const [mensaje, setMensaje] = useState(null);
  const [error, setError] = useState(null);

  // Cargar materia prima al iniciar
  const cargarMateriaPrima = async () => {
    setError(null);
    try {
      const response = await getMateriaPrima();
      setMateriaPrima(response.data);
    } catch (err) {
      console.error("Error al cargar materia prima:", err.message);
      setError("Error al cargar la materia prima.");
    }
  };

  useEffect(() => {
    cargarMateriaPrima();
  }, []);

  // Crear materia prima
  const handleCrearMateria = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);

    try {
      await crearMateriaPrima(nuevaMateria);
      setMensaje("Materia prima creada exitosamente.");
      setNuevaMateria({ nombre: "", cantidad_disponible: "", precio_por_unidad: "", producto_id: "" });
      cargarMateriaPrima(); // Recargar lista
    } catch (err) {
      console.error("Error al crear materia prima:", err.message);
      setError("Error al crear la materia prima.");
    }
  };

  // Actualizar materia prima
  const handleActualizarMateria = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);

    try {
      await actualizarMateriaPrima(materiaSeleccionada.id, materiaSeleccionada);
      setMensaje("Materia prima actualizada exitosamente.");
      setMateriaSeleccionada(null);
      cargarMateriaPrima(); // Recargar lista
    } catch (err) {
      console.error("Error al actualizar materia prima:", err.message);
      setError("Error al actualizar la materia prima.");
    }
  };

  // Eliminar materia prima
  const handleEliminarMateria = async (id) => {
    setError(null);
    setMensaje(null);

    try {
      await eliminarMateriaPrima(id);
      setMensaje("Materia prima eliminada correctamente.");
      cargarMateriaPrima(); // Recargar lista
    } catch (err) {
      console.error("Error al eliminar materia prima:", err.message);
      setError("Error al eliminar la materia prima.");
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Gestión de Materia Prima</h2>
      <p style={styles.subtitle}>Crea, actualiza o elimina materia prima.</p>

      {mensaje && <p style={styles.success}>{mensaje}</p>}
      {error && <p style={styles.error}>{error}</p>}

      {/* Formulario para crear o editar materia prima */}
      <form onSubmit={materiaSeleccionada ? handleActualizarMateria : handleCrearMateria} style={styles.form}>
        <h3>{materiaSeleccionada ? "Editar Materia Prima" : "Crear Materia Prima"}</h3>
        <input
          type="text"
          placeholder="Nombre"
          value={materiaSeleccionada ? materiaSeleccionada.nombre : nuevaMateria.nombre}
          onChange={(e) =>
            materiaSeleccionada
              ? setMateriaSeleccionada({ ...materiaSeleccionada, nombre: e.target.value })
              : setNuevaMateria({ ...nuevaMateria, nombre: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Cantidad Disponible"
          value={materiaSeleccionada ? materiaSeleccionada.cantidad_disponible : nuevaMateria.cantidad_disponible}
          onChange={(e) =>
            materiaSeleccionada
              ? setMateriaSeleccionada({ ...materiaSeleccionada, cantidad_disponible: e.target.value })
              : setNuevaMateria({ ...nuevaMateria, cantidad_disponible: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Precio por Unidad"
          value={materiaSeleccionada ? materiaSeleccionada.precio_por_unidad : nuevaMateria.precio_por_unidad}
          onChange={(e) =>
            materiaSeleccionada
              ? setMateriaSeleccionada({ ...materiaSeleccionada, precio_por_unidad: e.target.value })
              : setNuevaMateria({ ...nuevaMateria, precio_por_unidad: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Producto ID"
          value={materiaSeleccionada ? materiaSeleccionada.producto_id : nuevaMateria.producto_id}
          onChange={(e) =>
            materiaSeleccionada
              ? setMateriaSeleccionada({ ...materiaSeleccionada, producto_id: e.target.value })
              : setNuevaMateria({ ...nuevaMateria, producto_id: e.target.value })
          }
          style={styles.input}
          required
        />
        <button type="submit" style={styles.button}>
          {materiaSeleccionada ? "Actualizar Materia Prima" : "Crear Materia Prima"}
        </button>
      </form>

      {/* Listado de materia prima */}
      <h3>Listado de Materia Prima</h3>
      <ul style={styles.list}>
        {materiaPrima.map((materia) => (
          <li key={materia.id} style={styles.listItem}>
            <strong>{materia.nombre}</strong> - Cantidad: {materia.cantidad_disponible} - Precio: ${materia.precio_por_unidad} - Producto ID: {materia.producto_id}
            <button onClick={() => setMateriaSeleccionada(materia)} style={styles.editButton}>
              Editar
            </button>
            <button onClick={() => handleEliminarMateria(materia.id)} style={styles.deleteButton}>
              Eliminar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "800px",
    margin: "30px auto",
    padding: "20px",
    textAlign: "center",
    backgroundColor: "#664242",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
  },
  title: { fontSize: "2rem", marginBottom: "10px", color: "#fff" },
  subtitle: { fontSize: "1.2rem", marginBottom: "20px", color: "#fff" },
  form: { display: "flex", flexDirection: "column", gap: "10px", marginBottom: "20px" },
  input: { padding: "8px", border: "1px solid #ccc", borderRadius: "5px" },
  button: { padding: "10px", backgroundColor: "#007bff", color: "#fff", border: "none", borderRadius: "5px", cursor: "pointer" },
  list: { listStyleType: "none", padding: 0 },
  listItem: { marginBottom: "10px", display: "flex", justifyContent: "space-between", alignItems: "center" },
  editButton: { marginLeft: "10px", backgroundColor: "#ffc107", color: "#fff", border: "none", padding: "5px 10px", borderRadius: "5px" },
  deleteButton: { marginLeft: "10px", backgroundColor: "#dc3545", color: "#fff", border: "none", padding: "5px 10px", borderRadius: "5px" },
  success: { color: "green" },
  error: { color: "red" },
};

export default AdminMateriaPrima;
