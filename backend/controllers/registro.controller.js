import bcrypt from "bcrypt";
import Usuario from "../models/user.js";

export const registro = async (req, res) => {
  try {
    let { nombre, apellido, correo, telefono, password } = req.body;

    // 🔥 NORMALIZACIÓN
    nombre = nombre?.trim() || "";
    apellido = apellido?.trim() || "";
    correo = correo?.toLowerCase().trim() || "";
    telefono = telefono?.trim() || "";
    password = password || "";

    // 🔥 VALIDACIONES
    if (!nombre || !apellido || !correo || !telefono || !password) {
      return res.status(400).json({
        mensaje: "Todos los campos son obligatorios"
      });
    }

    const regexCorreo = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    if (!regexCorreo.test(correo)) {
      return res.status(400).json({
        mensaje: "El correo debe ser @gmail.com válido"
      });
    }

    if (!/^\d{10}$/.test(telefono)) {
      return res.status(400).json({
        mensaje: "El teléfono debe tener exactamente 10 dígitos"
      });
    }

    if (
      password.length < 6 ||
      !/[0-9]/.test(password) ||
      !/[a-zA-Z]/.test(password)
    ) {
      return res.status(400).json({
        mensaje: "La contraseña debe tener mínimo 6 caracteres, una letra y un número"
      });
    }

    // 🔥 VERIFICAR EXISTENTE
    const existe = await Usuario.findOne({ correo });

    if (existe) {
      return res.status(400).json({
        mensaje: "El correo ya está registrado"
      });
    }

    // 🔥 HASH PASSWORD
    const hash = await bcrypt.hash(password, 10);

    // 🔥 GUARDAR
    const nuevoUsuario = new Usuario({
      nombre,
      correo,
      password: hash
    });

    await nuevoUsuario.save();

    return res.status(200).json({
      mensaje: "Usuario registrado correctamente"
    });

  } catch (error) {
    console.error("Error en registro:", error);

    return res.status(500).json({
      mensaje: "Error en registro"
    });
  }
};


export const checkEmail = async (req, res) => {
  try {
    const correo = req.params.correo.toLowerCase().trim();

    const user = await Usuario.findOne({ correo });

    res.json({
      existe: user ? true : false
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({
      mensaje: "Error verificando correo"
    });
  }
};