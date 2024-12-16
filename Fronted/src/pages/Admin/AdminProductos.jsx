import { useState, useEffect } from "react";
import {
  getProductos,
  crearProducto,
  actualizarProducto,
  eliminarProducto,
} from "../../services/api";

const AdminProductos = () => {
  const [productos, setProductos] = useState([]); // Lista de productos
  const [formProducto, setFormProducto] = useState({
    nombre: "",
    descripcion: "",
    precio_unitario: "",
    stock: "",
  }); // Datos del formulario
  const [productoSeleccionado, setProductoSeleccionado] = useState(null); // Producto en edición
  const [mensaje, setMensaje] = useState(null); // Mensaje de éxito
  const [error, setError] = useState(null); // Mensaje de error
  const [isLoading, setIsLoading] = useState(false); // Estado de carga

  // Cargar productos al inicio
  useEffect(() => {
    cargarProductos();
  }, []);

 const cargarProductos = async () => {
  setIsLoading(true);
  setError(null);
  try {
    const response = await getProductos();
    console.log("Respuesta del backend (sin procesar):", response.data);

    // Parsear manualmente la respuesta si es un string
    const datos = typeof response.data === "string" ? JSON.parse(response.data) : response.data;

    // Verificar si la respuesta es un array
    if (Array.isArray(datos)) {
      const productosTransformados = datos.map((producto) => ({
        id: producto.id,
        nombre: producto.nombre_producto, // Renombrar clave
        descripcion: producto.descripcion,
        precio_unitario: producto.precio_unitario,
        stock: producto.stock,
        fecha_agregado: producto.fecha_agregado,
      }));
      setProductos(productosTransformados);
    } else {
      console.error("La respuesta del servidor no es un array:", datos);
      setError("Error: la respuesta del servidor no es válida.");
      setProductos([]);
    }
  } catch (error) {
    console.error("Error al cargar productos:", error.message);
    setError("No se pudieron cargar los productos.");
    setProductos([]);
  } finally {
    setIsLoading(false);
  }
};


  // Manejar cambios en el formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormProducto({ ...formProducto, [name]: value });
  };

  // Crear o actualizar producto
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje(null);
    setError(null);
    try {
      if (productoSeleccionado) {
        // Actualizar producto
        await actualizarProducto({ ...formProducto, id: productoSeleccionado.id });
        setMensaje("Producto actualizado exitosamente.");
      } else {
        // Crear producto
        await crearProducto(formProducto);
        setMensaje("Producto creado exitosamente.");
      }
      setFormProducto({ nombre: "", descripcion: "", precio_unitario: "", stock: "" });
      setProductoSeleccionado(null);
      cargarProductos(); // Recargar productos
    } catch (error) {
      console.error("Error al guardar producto:", error.message);
      setError("No se pudo guardar el producto.");
    }
  };

  // Eliminar producto
  const handleEliminar = async (id) => {
    if (!window.confirm("¿Estás seguro de eliminar este producto?")) return;
    setError(null);
    setMensaje(null);
    try {
      await eliminarProducto(id);
      setMensaje("Producto eliminado exitosamente.");
      cargarProductos();
    } catch (error) {
      console.error("Error al eliminar producto:", error.message);
      setError("No se pudo eliminar el producto.");
    }
  };

  // Manejar selección de producto para edición
  const handleEditar = (producto) => {
    setProductoSeleccionado(producto);
    setFormProducto(producto);
  };

  // Cancelar edición
  const handleCancelar = () => {
    setProductoSeleccionado(null);
    setFormProducto({ nombre: "", descripcion: "", precio_unitario: "", stock: "" });
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Administrar Productos</h1>
      {mensaje && <p style={styles.success}>{mensaje}</p>}
      {error && <p style={styles.error}>{error}</p>}
      <form onSubmit={handleSubmit} style={styles.form}>
        <h3>{productoSeleccionado ? "Editar Producto" : "Crear Producto"}</h3>
        <input
          type="text"
          name="nombre"
          placeholder="Nombre"
          value={formProducto.nombre}
          onChange={handleChange}
          style={styles.input}
          required
        />
        <input
          type="text"
          name="descripcion"
          placeholder="Descripción"
          value={formProducto.descripcion}
          onChange={handleChange}
          style={styles.input}
          required
        />
        <input
          type="number"
          name="precio_unitario"
          placeholder="Precio Unitario"
          value={formProducto.precio_unitario}
          onChange={handleChange}
          style={styles.input}
          required
        />
        <input
          type="number"
          name="stock"
          placeholder="Stock"
          value={formProducto.stock}
          onChange={handleChange}
          style={styles.input}
          required
        />
        <div style={styles.actions}>
          <button type="submit" style={styles.button}>
            {productoSeleccionado ? "Actualizar" : "Crear"}
          </button>
          {productoSeleccionado && (
            <button type="button" onClick={handleCancelar} style={styles.cancelButton}>
              Cancelar
            </button>
          )}
        </div>
      </form>
      <h3>Listado de Productos</h3>
      {isLoading ? (
        <p>Cargando productos...</p>
      ) : productos.length > 0 ? (
        <ul style={styles.list}>
          {productos.map((producto) => (
            <li key={producto.id} style={styles.listItem}>
              <span>
                <strong>{producto.nombre}</strong> - {producto.descripcion} - ${producto.precio_unitario} - Stock:{" "}
                {producto.stock}
              </span>
              <div>
                <button onClick={() => handleEditar(producto)} style={styles.editButton}>
                  Editar
                </button>
                <button onClick={() => handleEliminar(producto.id)} style={styles.deleteButton}>
                  Eliminar
                </button>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay productos disponibles.</p>
      )}
    </div>
  );
};

const styles = {
  container: { maxWidth: "800px", margin: "20px auto", padding: "20px", textAlign: "center" },
  title: { fontSize: "2rem", marginBottom: "10px" },
  success: { color: "green" },
  error: { color: "red" },
  form: { marginBottom: "20px", display: "flex", flexDirection: "column", gap: "10px" },
  input: { padding: "10px", border: "1px solid #ccc", borderRadius: "5px" },
  actions: { display: "flex", gap: "10px", justifyContent: "center" },
  button: { padding: "10px", backgroundColor: "#007bff", color: "#fff", borderRadius: "5px", cursor: "pointer" },
  cancelButton: { padding: "10px", backgroundColor: "#6c757d", color: "#fff", borderRadius: "5px", cursor: "pointer" },
  list: { listStyle: "none", padding: "0" },
  listItem: { marginBottom: "10px", display: "flex", justifyContent: "space-between", alignItems: "center" },
  editButton: { marginRight: "10px", backgroundColor: "#ffc107", color: "#fff", borderRadius: "5px", cursor: "pointer" },
  deleteButton: { backgroundColor: "#dc3545", color: "#fff", borderRadius: "5px", cursor: "pointer" },
};

export default AdminProductos;
