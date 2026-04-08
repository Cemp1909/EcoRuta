import express from "express";
import { registro, checkEmail } from "../controllers/registro.controller.js";
import { login } from "../controllers/login.controller.js";

const router = express.Router();

router.get("/check-email/:correo", checkEmail);
router.post("/registro", registro);
router.post("/login", login);

export default router;