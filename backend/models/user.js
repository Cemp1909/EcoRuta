import mongoose from "mongoose";

const usuarioSchema = new mongoose.Schema({
  nombre: String,
  correo: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  }
});

export default mongoose.model("Usuario", usuarioSchema);