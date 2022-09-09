import * as THREE from "https://threejsfundamentals.org/threejs/resources/threejs/r125/build/three.module.js";
import { TrackballControls } from "https://threejsfundamentals.org/threejs/resources/threejs/r125/examples/jsm/controls/TrackballControls.js";
import { Lut } from "https://threejsfundamentals.org/threejs/resources/threejs/r125/examples/jsm/math/Lut.js";

// global variables needed for animation/interaction
let renderer;
let controls;
let camera;
let scene;
let cursor;
let raycaster;
let selectedSphere = null;
let dataList;

// entry point
init();
buildScene();
camera.position.set(-20, 20, 80);
camera.lookAt(-50, 0, 50);
animate();

function init() {
    const container = initContainer("threejs-container");
    renderer = initRenderer(container);
    camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 1, 400);
    controls = initControls(camera, renderer);
    cursor = new THREE.Vector2();
    cursor.set({ x: -99, y: 99 });
    container.addEventListener("pointermove", onCursorMove);
    raycaster = new THREE.Raycaster();
}

function initContainer(divId) {
    const div = document.getElementById(divId);
    return div;
}

function initRenderer(container) {
    const rend = new THREE.WebGLRenderer();
    rend.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(rend.domElement);
    return rend;
}

function initControls(camera, renderer) {
    const ctrl = new TrackballControls(camera, renderer.domElement);
    ctrl.rotateSpeed = 2.0;
    return ctrl;
}

async function readData(source="encoded_faces.json", colorMap="hot") {
    let jsonContent = await (await fetch(source)).json();
    let result = [];
    let minX = Number.MAX_VALUE;
    let maxX = Number.MIN_VALUE;
    for (const name in jsonContent) {
        const info = jsonContent[name];
        const ele = {
            name: name,
            x: info["pca"][0],
            y: info["pca"][1],
            z: info["pca"][2],
            link: info["link"],
            b64: info["b64"],
        };
        if (ele.x < minX) { minX = ele.x; }
        if (ele.x > maxX) { maxX = ele.x; }
        result.push(ele);
    }

    // determine colors
    const lut = new Lut(colorMap, result.length);
    for (let i = 0; i < result.length; i++) {
        let xVal = (result[i].x - minX) / (maxX - minX);
        xVal = xVal * 0.8 + 0.1;
        result[i].color = lut.getColor(xVal);
    }

    return result;
}

async function buildScene() {
    scene = new THREE.Scene();

    const light = new THREE.DirectionalLight("white", 0.8);
    scene.add(light);

    const fog = new THREE.Fog("black", 0.05, 200);
    scene.fog = fog;

    dataList = await readData();
    const scalar = -100;
    for (let iData = 0; iData < dataList.length; iData++) {
        const data = dataList[iData];
        const geometry = new THREE.SphereGeometry(1, 64, 32);
        const material = new THREE.MeshStandardMaterial({ emissive: data.color, emissiveIntensity: 0.7 });
        const sphere = new THREE.Mesh(geometry, material);
        sphere.link = data.link;
        sphere.position.set(scalar * data.x, scalar * data.y, scalar * data.z);
        scene.add(sphere);
    }

    const gridXZ = new THREE.GridHelper(100, 10, "white", "white");
    gridXZ.position.x = 0;
    gridXZ.position.y = -50;
    gridXZ.position.z = 0;
    gridXZ.rotation.y = Math.PI / 2;
    scene.add(gridXZ);

    const gridXY = new THREE.GridHelper(100, 10, "white", "white");
    gridXY.position.x = -50;
    gridXY.position.y = 0;
    gridXY.position.z = 0;
    gridXY.rotation.z = Math.PI / 2;
    scene.add(gridXY);
}

function updateHovered() {
    if (selectedSphere) {
        const index = scene.children.indexOf(selectedSphere) - 1;

        const img = document.getElementById("hovered-img");
        img.src = dataList[index].b64;
        img.alt = dataList[index].name;

        const linkHref = document.getElementById("hovered-link");
        linkHref.href = dataList[index].link;

        const nameDiv = document.getElementById("hovered-name");
        nameDiv.innerText = dataList[index].name;

        const pcaDiv = document.getElementById("hovered-pca");
        pcaDiv.innerText = `PCA = (${dataList[index].x.toFixed(4)}, ${dataList[index].y.toFixed(4)}, ${dataList[index].z.toFixed(4)})`;
    }
}

function onCursorMove(event) {
    cursor.x = ((event.clientX - renderer.domElement.offsetLeft) / renderer.domElement.clientWidth) * 2 - 1;
    cursor.y = -((event.clientY - renderer.domElement.offsetTop) / renderer.domElement.clientHeight) * 2 + 1;
}

function render() {
    // identify hover object
    raycaster.setFromCamera(cursor, camera);
    const intersects = raycaster.intersectObjects(scene.children, false);
    if (intersects.length > 0) {
        if (selectedSphere != intersects[0].object) {
            if (selectedSphere) {
                selectedSphere.material.emissiveIntensity = selectedSphere.prevEmissiveIntensity;
            }
            selectedSphere = intersects[0].object;
            selectedSphere.prevEmissiveIntensity = selectedSphere.material.emissiveIntensity;
            selectedSphere.material.emissiveIntensity = 2 * selectedSphere.material.emissiveIntensity;
        }
    } else {
        if (selectedSphere) {
            selectedSphere.material.emissiveIntensity = selectedSphere.prevEmissiveIntensity;
        }
        selectedSphere = null;
    }

    updateHovered();

    renderer.render(scene, camera);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    render();
};
