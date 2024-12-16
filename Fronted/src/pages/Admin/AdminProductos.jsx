import { useState, useEffect } from "react";
import { getProductos, crearProducto, actualizarProducto, eliminarProducto } from "../../services/api";

const AdminProductos = () => {
  const [productos, setProductos] = useState([]); // Lista de productos
  const [nuevoProducto, setNuevoProducto] = useState({
    nombre: "",
    descripcion: "",
    precio_unitario: "",
    stock: "",
  });
  const [productoSeleccionado, setProductoSeleccionado] = useState(null); // Producto en edición
  const [mensaje, setMensaje] = useState(null);
  const [error, setError] = useState(null);

  // Cargar productos al iniciar
  const cargarProductos = async () => {
    setError(null);
    try {
      const response = await getProductos();
      setProductos(response.data);
    } catch (error) {
      console.error("Error al cargar productos:", error.message);
      setError("Error al cargar los productos.");
    }
  };

  useEffect(() => {
    cargarProductos();
  }, []);

  // Crear un producto
  const handleCrearProducto = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);
    try {
      await crearProducto(nuevoProducto);
      setMensaje("Producto creado exitosamente.");
      setNuevoProducto({ nombre: "", descripcion: "", precio_unitario: "", stock: "" });
      cargarProductos(); // Recargar productos
    } catch (error) {
      console.error("Error al crear producto:", error.message);
      setError("Error al crear el producto.");
    }
  };

  // Editar un producto
  const handleActualizarProducto = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);
    try {
      await actualizarProducto(productoSeleccionado);
      setMensaje("Producto actualizado exitosamente.");
      setProductoSeleccionado(null);
      cargarProductos(); // Recargar productos
    } catch (error) {
      console.error("Error al actualizar producto:", error.message);
      setError("Error al actualizar el producto.");
    }
  };

  // Eliminar un producto
  const handleEliminarProducto = async (id) => {
    setError(null);
    setMensaje(null);
    try {
      await eliminarProducto(id);
      setMensaje("Producto eliminado correctamente.");
      cargarProductos(); // Recargar productos
    } catch (error) {
      console.error("Error al eliminar producto:", error.message);
      setError("Error al eliminar el producto.");
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Gestión de Productos</h2>
      <p style={styles.subtitle}>Crea, actualiza o elimina productos fácilmente.</p>

      {mensaje && <p style={styles.success}>{mensaje}</p>}
      {error && <p style={styles.error}>{error}</p>}

      {/* Formulario para crear o editar productos */}
      <form onSubmit={productoSeleccionado ? handleActualizarProducto : handleCrearProducto} style={styles.form}>
        <h3>{productoSeleccionado ? "Editar Producto" : "Crear Producto"}</h3>
        <input
          type="text"
          placeholder="Nombre"
          value={productoSeleccionado ? productoSeleccionado.nombre : nuevoProducto.nombre}
          onChange={(e) =>
            productoSeleccionado
              ? setProductoSeleccionado({ ...productoSeleccionado, nombre: e.target.value })
              : setNuevoProducto({ ...nuevoProducto, nombre: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="text"
          placeholder="Descripción"
          value={productoSeleccionado ? productoSeleccionado.descripcion : nuevoProducto.descripcion}
          onChange={(e) =>
            productoSeleccionado
              ? setProductoSeleccionado({ ...productoSeleccionado, descripcion: e.target.value })
              : setNuevoProducto({ ...nuevoProducto, descripcion: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Precio Unitario"
          value={productoSeleccionado ? productoSeleccionado.precio_unitario : nuevoProducto.precio_unitario}
          onChange={(e) =>
            productoSeleccionado
              ? setProductoSeleccionado({ ...productoSeleccionado, precio_unitario: e.target.value })
              : setNuevoProducto({ ...nuevoProducto, precio_unitario: e.target.value })
          }
          style={styles.input}
          required
        />
        <input
          type="number"
          placeholder="Stock"
          value={productoSeleccionado ? productoSeleccionado.stock : nuevoProducto.stock}
          onChange={(e) =>
            productoSeleccionado
              ? setProductoSeleccionado({ ...productoSeleccionado, stock: e.target.value })
              : setNuevoProducto({ ...nuevoProducto, stock: e.target.value })
          }
          style={styles.input}
          required
        />
        <button type="submit" style={styles.button}>
          {productoSeleccionado ? "Actualizar Producto" : "Crear Producto"}
        </button>
      </form>

      {/* Listado de productos */}
      <h3>Listado de Productos</h3>
      <ul style={styles.list}>
        {productos.map((producto) => (
          <li key={producto.id} style={styles.listItem}>
            <strong>{producto.nombre}</strong> - {producto.descripcion} - ${producto.precio_unitario} - Stock: {producto.stock}
            <button onClick={() => setProductoSeleccionado(producto)} style={styles.editButton}>
              Editar
            </button>
            <button onClick={() => handleEliminarProducto(producto.id)} style={styles.deleteButton}>
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
    backgroundColor: "#f9f9f9",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
  },
  title: { fontSize: "2rem", marginBottom: "10px", color: "#333" },
  subtitle: { fontSize: "1.2rem", marginBottom: "20px", color: "#555" },
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

export default AdminProductos;
