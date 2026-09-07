import * as THREE from './vendor/three/three.module.min.js';

// A line-only renderer for browsers without WebGL. It uses the same scene,
// orthographic camera, world-space geometry and OrbitControls as the GPU view.
export class CanvasLineRenderer {
  constructor(canvas) {
    this.context = canvas.getContext('2d');
    if (!this.context) throw new Error('Canvas rendering is unavailable');
    this.canvas = canvas;
    this.pixelRatio = 1;
    this.width = 1;
    this.height = 1;
    this.background = '#fafcfe';
    this.matrix = new THREE.Matrix4();
    this.viewProjection = new THREE.Matrix4();
    this.pointA = new THREE.Vector3();
    this.pointB = new THREE.Vector3();
    this.color = new THREE.Color();
    canvas.dataset.renderer = 'canvas3d';
  }

  setPixelRatio(ratio) { this.pixelRatio = ratio; }
  setClearColor(color) { this.background = new THREE.Color(color).getStyle(); }
  setSize(width, height) {
    this.width = width;
    this.height = height;
    this.canvas.width = Math.round(width * this.pixelRatio);
    this.canvas.height = Math.round(height * this.pixelRatio);
  }

  render(scene, camera) {
    const ctx = this.context;
    ctx.setTransform(this.pixelRatio, 0, 0, this.pixelRatio, 0, 0);
    ctx.globalAlpha = 1;
    ctx.fillStyle = this.background;
    ctx.fillRect(0, 0, this.width, this.height);
    ctx.lineWidth = 1.25;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    scene.updateMatrixWorld();
    camera.updateMatrixWorld();
    this.viewProjection.multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse);
    const objects = [];
    scene.traverseVisible((object) => { if (object.isLine) objects.push(object); });
    objects.sort((a, b) => a.renderOrder - b.renderOrder);
    const pixelsPerUnit = this.height / (camera.top - camera.bottom) * camera.zoom;

    for (const object of objects) {
      const material = object.material;
      const geometry = object.geometry;
      const position = geometry.getAttribute('position');
      if (!position || !material.visible || material.opacity <= 0) continue;
      const colors = material.vertexColors && geometry.getAttribute('color');
      const count = geometry.index ? geometry.index.count : position.count;
      const step = object.isLineSegments ? 2 : 1;
      const end = object.isLineLoop ? count : count - 1;
      this.matrix.multiplyMatrices(this.viewProjection, object.matrixWorld);
      ctx.globalAlpha = material.opacity;
      ctx.strokeStyle = material.color.getStyle();
      ctx.setLineDash(material.isLineDashedMaterial
        ? [Math.max(1, material.dashSize * pixelsPerUnit), Math.max(1, material.gapSize * pixelsPerUnit)] : []);
      ctx.beginPath();
      for (let i = 0; i < end; i += step) {
        const first = geometry.index ? geometry.index.getX(i) : i;
        const nextIndex = (i + 1) % count;
        const second = geometry.index ? geometry.index.getX(nextIndex) : nextIndex;
        this.pointA.fromBufferAttribute(position, first).applyMatrix4(this.matrix);
        this.pointB.fromBufferAttribute(position, second).applyMatrix4(this.matrix);
        if ((this.pointA.z < -1 && this.pointB.z < -1) || (this.pointA.z > 1 && this.pointB.z > 1)) continue;
        if (colors) {
          ctx.beginPath();
          ctx.strokeStyle = this.color.fromBufferAttribute(colors, first).getStyle();
        }
        ctx.moveTo((this.pointA.x + 1) * this.width / 2, (1 - this.pointA.y) * this.height / 2);
        ctx.lineTo((this.pointB.x + 1) * this.width / 2, (1 - this.pointB.y) * this.height / 2);
        if (colors) ctx.stroke();
      }
      if (!colors) ctx.stroke();
    }
    ctx.globalAlpha = 1;
    ctx.setLineDash([]);
  }
}
