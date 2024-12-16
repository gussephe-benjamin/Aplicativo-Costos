import { useEffect, useState } from "react";
import { crearOrden, getOrdenes, eliminarOrden } from "../services/api";

const Ordenes = () => {
  const [ordenes, setOrdenes] = useState([]); // Almacena las órdenes existentes
  const [nuevaOrden, setNuevaOrden] = useState({
    usuario_id: "",
    producto_id: "",
    cantidad: "",
    fecha_entrega: "",
  });
  const [error, setError] = useState(null);
  const [mensaje, setMensaje] = useState(null);

  // Cargar las órdenes existentes al iniciar
  const cargarOrdenes = async () => {
    try {
      const response = await getOrdenes();
      setOrdenes(response.data);
    } catch (error) {
      console.error("Error al cargar órdenes:", error.message);
      setError("Error al cargar las órdenes.");
    }
  };

  useEffect(() => {
    cargarOrdenes();
  }, []);

  // Manejar la creación de una nueva orden
  const handleCrearOrden = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);
  
    console.log("Datos enviados al backend:", nuevaOrden);
  
    try {
      await crearOrden(nuevaOrden);
      setMensaje("Orden creada exitosamente.");
      setNuevaOrden({
        usuario_id: "",
        producto_id: "",
        cantidad: "",
        fecha_entrega: "",
      });
      cargarOrdenes(); // Recargar las órdenes
    } catch (error) {
      console.error("Error al crear orden:", error.response?.data || error.message);
      setError("Error al crear la orden. Verifique los datos.");
    }
  };
  

  // Manejar la eliminación de una orden
  const handleEliminarOrden = async (id) => {
    try {
      await eliminarOrden(id);
      setMensaje("Orden eliminada correctamente.");
      cargarOrdenes(); // Recargar las órdenes
    } catch (error) {
      console.error("Error al eliminar orden:", error.message);
      setError("Error al eliminar la orden.");
    }
  };

  return (
    <div style={styles.container}>
      <h2>Gestión de Órdenes</h2>

      {/* Formulario para crear una nueva orden */}
      <form onSubmit={handleCrearOrden} style={styles.form}>
        <h3>Crear Nueva Orden</h3>

        <label>Usuario ID:</label>
        <input
          type="number"
          value={nuevaOrden.usuario_id}
          onChange={(e) =>
            setNuevaOrden({ ...nuevaOrden, usuario_id: e.target.value })
          }
          style={styles.input}
          required
        />

        <label>Producto ID:</label>
        <input
          type="number"
          value={nuevaOrden.producto_id}
          onChange={(e) =>
            setNuevaOrden({ ...nuevaOrden, producto_id: e.target.value })
          }
          style={styles.input}
          required
        />

        <label>Cantidad:</label>
        <input
          type="number"
          value={nuevaOrden.cantidad}
          onChange={(e) =>
            setNuevaOrden({ ...nuevaOrden, cantidad: e.target.value })
          }
          style={styles.input}
          required
        />

        <label>Fecha de Entrega:</label>
        <input
          type="date"
          value={nuevaOrden.fecha_entrega}
          onChange={(e) =>
            setNuevaOrden({ ...nuevaOrden, fecha_entrega: e.target.value })
          }
          style={styles.input}
          required
        />

        <button type="submit" style={styles.button}>
          Crear Orden
        </button>
      </form>

      {/* Mensajes de éxito o error */}
      {mensaje && <p style={styles.success}>{mensaje}</p>}
      {error && <p style={styles.error}>{error}</p>}

      {/* Listado de órdenes existentes */}
      <h3>Órdenes Existentes</h3>
      <ul style={styles.list}>
        {ordenes.map((orden) => (
          <li key={orden.id} style={styles.listItem}>
            <strong>ID:</strong> {orden.id} | <strong>Usuario ID:</strong>{" "}
            {orden.usuario_id} | <strong>Producto ID:</strong>{" "}
            {orden.producto_id} | <strong>Cantidad:</strong> {orden.cantidad} |{" "}
            <strong>Fecha de Entrega:</strong> {orden.fecha_entrega}
            <button
              onClick={() => handleEliminarOrden(orden.id)}
              style={styles.deleteButton}
            >
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
    maxWidth: "600px",
    margin: "30px auto",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
    backgroundColor: "#664242",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    marginBottom: "20px",
  },
  input: {
    padding: "8px",
    border: "1px solid #ccc",
    borderRadius: "5px",
  },
  button: {
    backgroundColor: "#007bff",
    color: "#fff",
    padding: "10px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  },
  deleteButton: {
    marginLeft: "10px",
    padding: "5px 10px",
    backgroundColor: "#dc3545",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  success: { color: "green", marginTop: "10px" },
  error: { color: "red", marginTop: "10px" },
  list: { listStyleType: "none", padding: 0 },
  listItem: {
    marginBottom: "10px",
    padding: "10px",
    backgroundColor: "#23ff00",
    borderRadius: "5px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
};

export default Ordenes;
