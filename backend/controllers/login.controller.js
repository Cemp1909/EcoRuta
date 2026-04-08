import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import Usuario from "../models/user.js";

export const login = async (req, res) => {
  try {
    const { correo, password } = req.body;

    const user = await Usuario.findOne({ correo });

    if (!user) {
      return res.status(404).json({ mensaje: "Usuario no encontrado" });
    }

    const valido = await bcrypt.compare(password, user.password);

    if (!valido) {
      return res.status(401).json({ mensaje: "Contraseña incorrecta" });
    }

    const token = jwt.sign(
      { id: user._id, correo: user.correo },
      process.env.JWT_SECRET,
      { expiresIn: "7d" }
    );

    res.json({
      mensaje: "Login exitoso",
      token,
      usuario: {
        nombre: user.nombre,
        correo: user.correo
      }
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({ mensaje: "Error en login" });
  }
};