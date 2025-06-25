export interface DetalleIngreso {
  id?: number;
  producto_id: number;
  cantidad_fardos_paquetes: number;
  unidades_por_fardo_paquete: number;
  unidades_totales?: number;
  usuario_creacion?: string;
  fecha_creacion?: string;
  usuario_modificacion?: string;
  fecha_modificacion?: string;
}

export interface IngresoMercancia {
  id?: number;
  fecha_ingreso: string;
  numero_contenedor: string;
  numero_duca: string;
  fecha_duca: string;
  numero_duca_rectificada?: string;
  fecha_duca_rectificada?: string;
  observaciones?: string;
  estado?: string;
  usuario_creacion?: string;
  fecha_creacion?: string;
  usuario_modificacion?: string;
  fecha_modificacion?: string;
  usuario_confirmacion?: string;
  fecha_confirmacion?: string;
  detalles: DetalleIngreso[];
}

export interface InventarioStock {
  id: number;
  producto_id: number;
  stock_total: number;
  stock_disponible: number;
  stock_apartado: number;
  fecha_ultima_actualizacion: string;
  usuario_ultima_actualizacion: string;
  producto: {
    id: number;
    codigo_producto: string;
    nombre_producto: string;
  };
}

export interface Inventario {
  id?: number;
  fecha_ingreso: string;
  producto_id: number;
  cantidad_fardos_paquetes: number;
  unidades_por_fardo_paquete: number;
  unidades_totales: number;
  numero_contenedor: string;
  numero_duca: string;
  fecha_duca: string;
  numero_duca_rectificada?: string;
  fecha_duca_rectificada?: string;
  observaciones?: string;
}