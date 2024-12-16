import { useState, useEffect } from "react";
import { getManoObra, crearManoObra, actualizarManoObra, eliminarManoObra } from "../../services/api";

const AdminManoObra = () => {
  const [manoObra, setManoObra] = useState([]); // Lista de mano de obra
  const [nuevaMano, setNuevaMano] = useState({
    nombre_empleado: "",
    costo_por_hora: "",
    horas_requeridas: "",
    producto_id: "",
  });
  const [manoSeleccionada, setManoSeleccionada] = useState(null); // Mano de obra en edición
  const [mensaje, setMensaje] = useState(null);
  const [error, setError] = useState(null);

  // Cargar mano de obra al iniciar
  const cargarManoObra = async () => {
    setError(null);
    try {
      const response = await getManoObra();
      setManoObra(response.data);
    } catch (err) {
      console.error("Error al cargar mano de obra:", err.message);
      setError("Error al cargar la mano de obra.");
    }
  };

  useEffect(() => {
    cargarManoObra();
  }, []);

  // Crear mano de obra
  const handleCrearManoObra = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);

    try {
      await crearManoObra(nuevaMano);
      setMensaje("Mano de obra creada exitosamente.");
      setNuevaMano({ nombre_empleado: "", costo_por_hora: "", horas_requeridas: "", producto_id: "" });
      cargarManoObra(); // Recargar lista
    } catch (err) {
      console.error("Error al crear mano de obra:", err.message);
      setError("Error al crear la mano de obra.");
    }
  };

  // Actualizar mano de obra
  const handleActualizarManoObra = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);

    try {
      await actualizarManoObra(manoSeleccionada.id, manoSeleccionada);
      setMensaje("Mano de obra actualizada exitosamente.");
      setManoSeleccionada(null);
      cargarManoObra(); // Recargar lista
    } catch (err) {
      console.error("Error al actualizar mano de obra:", err.message);
      setError("Error al actualizar la mano de obra.");
    }
  };

  // Eliminar mano de obra
  const handleEliminarManoObra = async (id) => {
    setError(null);
    setMensaje(null);

    try {
      await eliminarManoObra(id);
      setMensaje("Mano de obra eliminada correctamente.");
      cargarManoObra(); // Recargar lista
    } catch (err) {
      console.error("Error al eliminar mano de obra:", err.message);
      setError("Error al eliminar la mano de obra.");
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Gestión de Mano de Obra</h2>
      <p style={styles.subtitle}>Crea, actualiza o elimina registros de mano de obra.</p>

      {mensaje && <p style={styles.success}>{mensaje}</p>}
      {error && <p style={styles.error}>{error}</p>}

      {/* Formulario para crear o editar mano de obra */}
      <form onSubmit={manoSeleccionada ? handleActualizarManoObra : handleCrearManoObra} style={styles.form}>
        <h3>{manoSeleccionada ? "Editar Mano de Obra" : "Crear Mano de Obra"}</h3>
        <input
          type="text"
          placeholder="Nombre del Empleado"
          value={manoSeleccionada ? manoSeleccionada.nombre_empleado : nuevaMano.nombre_empleado}
          onChange={(e) =>
            manoSeleccionada
              ? setManoSeleccionada({ ...manoSeleccionada, nombre_empleado: e.target.value })
              : setNuevaMano({ ...nuevaMano, nombre_empleado: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Costo por Hora"
          value={manoSeleccionada ? manoSeleccionada.costo_por_hora : nuevaMano.costo_por_hora}
          onChange={(e) =>
            manoSeleccionada
              ? setManoSeleccionada({ ...manoSeleccionada, costo_por_hora: e.target.value })
              : setNuevaMano({ ...nuevaMano, costo_por_hora: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Horas Requeridas"
          value={manoSeleccionada ? manoSeleccionada.horas_requeridas : nuevaMano.horas_requeridas}
          onChange={(e) =>
            manoSeleccionada
              ? setManoSeleccionada({ ...manoSeleccionada, horas_requeridas: e.target.value })
              : setNuevaMano({ ...nuevaMano, horas_requeridas: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Producto ID"
          value={manoSeleccionada ? manoSeleccionada.producto_id : nuevaMano.producto_id}
          onChange={(e) =>
            manoSeleccionada
              ? setManoSeleccionada({ ...manoSeleccionada, producto_id: e.target.value })
              : setNuevaMano({ ...nuevaMano, producto_id: e.target.value })
          }
          style={styles.input}
          required
        />
        <button type="submit" style={styles.button}>
          {manoSeleccionada ? "Actualizar Mano de Obra" : "Crear Mano de Obra"}
        </button>
      </form>

      {/* Listado de mano de obra */}
      <h3>Listado de Mano de Obra</h3>
      <ul style={styles.list}>
        {manoObra.map((mano) => (
          <li key={mano.id} style={styles.listItem}>
            <strong>{mano.nombre_empleado}</strong> - Costo por Hora: ${mano.costo_por_hora} - Horas: {mano.horas_requeridas} - Producto ID: {mano.producto_id}
            <button onClick={() => setManoSeleccionada(mano)} style={styles.editButton}>
              Editar
            </button>
            <button onClick={() => handleEliminarManoObra(mano.id)} style={styles.deleteButton}>
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

export default AdminManoObra;
