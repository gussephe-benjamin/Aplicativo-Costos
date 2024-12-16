import { useState, useEffect } from "react";
import { getCostosIndirectos, crearCostoIndirecto, actualizarCostoIndirecto, eliminarCostoIndirecto } from "../../services/api";

const AdminCostosIndirectos = () => {
  const [costosIndirectos, setCostosIndirectos] = useState([]); // Lista de costos indirectos
  const [nuevoCosto, setNuevoCosto] = useState({
    tipo: "",
    monto: "",
    descripcion: "",
  });
  const [costoSeleccionado, setCostoSeleccionado] = useState(null); // Costo en edición
  const [mensaje, setMensaje] = useState(null);
  const [error, setError] = useState(null);

  // Cargar costos indirectos al iniciar
  const cargarCostosIndirectos = async () => {
    setError(null);
    try {
      const response = await getCostosIndirectos();
      setCostosIndirectos(response.data);
    } catch (err) {
      console.error("Error al cargar costos indirectos:", err.message);
      setError("Error al cargar los costos indirectos.");
    }
  };

  useEffect(() => {
    cargarCostosIndirectos();
  }, []);

  // Crear costo indirecto
  const handleCrearCostoIndirecto = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);

    try {
      await crearCostoIndirecto(nuevoCosto);
      setMensaje("Costo indirecto creado exitosamente.");
      setNuevoCosto({ tipo: "", monto: "", descripcion: "" });
      cargarCostosIndirectos(); // Recargar lista
    } catch (err) {
      console.error("Error al crear costo indirecto:", err.message);
      setError("Error al crear el costo indirecto.");
    }
  };

  // Actualizar costo indirecto
  const handleActualizarCostoIndirecto = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);

    try {
      await actualizarCostoIndirecto(costoSeleccionado.id, costoSeleccionado);
      setMensaje("Costo indirecto actualizado exitosamente.");
      setCostoSeleccionado(null);
      cargarCostosIndirectos(); // Recargar lista
    } catch (err) {
      console.error("Error al actualizar costo indirecto:", err.message);
      setError("Error al actualizar el costo indirecto.");
    }
  };

  // Eliminar costo indirecto
  const handleEliminarCostoIndirecto = async (id) => {
    setError(null);
    setMensaje(null);

    try {
      await eliminarCostoIndirecto(id);
      setMensaje("Costo indirecto eliminado correctamente.");
      cargarCostosIndirectos(); // Recargar lista
    } catch (err) {
      console.error("Error al eliminar costo indirecto:", err.message);
      setError("Error al eliminar el costo indirecto.");
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Gestión de Costos Indirectos</h2>
      <p style={styles.subtitle}>Crea, actualiza o elimina registros de costos indirectos.</p>

      {mensaje && <p style={styles.success}>{mensaje}</p>}
      {error && <p style={styles.error}>{error}</p>}

      {/* Formulario para crear o editar costos indirectos */}
      <form onSubmit={costoSeleccionado ? handleActualizarCostoIndirecto : handleCrearCostoIndirecto} style={styles.form}>
        <h3>{costoSeleccionado ? "Editar Costo Indirecto" : "Crear Costo Indirecto"}</h3>
        <input
          type="text"
          placeholder="Tipo de Costo"
          value={costoSeleccionado ? costoSeleccionado.tipo : nuevoCosto.tipo}
          onChange={(e) =>
            costoSeleccionado
              ? setCostoSeleccionado({ ...costoSeleccionado, tipo: e.target.value })
              : setNuevoCosto({ ...nuevoCosto, tipo: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Monto"
          value={costoSeleccionado ? costoSeleccionado.monto : nuevoCosto.monto}
          onChange={(e) =>
            costoSeleccionado
              ? setCostoSeleccionado({ ...costoSeleccionado, monto: e.target.value })
              : setNuevoCosto({ ...nuevoCosto, monto: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="text"
          placeholder="Descripción"
          value={costoSeleccionado ? costoSeleccionado.descripcion : nuevoCosto.descripcion}
          onChange={(e) =>
            costoSeleccionado
              ? setCostoSeleccionado({ ...costoSeleccionado, descripcion: e.target.value })
              : setNuevoCosto({ ...nuevoCosto, descripcion: e.target.value })
          }
          style={styles.input}
          required
        />
        <button type="submit" style={styles.button}>
          {costoSeleccionado ? "Actualizar Costo Indirecto" : "Crear Costo Indirecto"}
        </button>
      </form>

      {/* Listado de costos indirectos */}
      <h3>Listado de Costos Indirectos</h3>
      <ul style={styles.list}>
        {costosIndirectos.map((costo) => (
          <li key={costo.id} style={styles.listItem}>
            <strong>{costo.tipo}</strong> - Monto: ${costo.monto} - {costo.descripcion}
            <button onClick={() => setCostoSeleccionado(costo)} style={styles.editButton}>
              Editar
            </button>
            <button onClick={() => handleEliminarCostoIndirecto(costo.id)} style={styles.deleteButton}>
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

export default AdminCostosIndirectos;
