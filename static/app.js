let scene;
let camera;
let renderer;

function main() {
    const canvas = document.querySelector('#c');
    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 2;
    scene.add(camera);

    // Set up renderer with transparency
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    const textureLoader = new THREE.TextureLoader();

    // Earth Geometry
    const earthGeometry = new THREE.SphereGeometry(0.6, 32, 32);
    const earthMaterial = new THREE.MeshPhongMaterial({
        roughness: 1,
        metalness: 0,
        map: textureLoader.load('/static/img/earthmap1k.jpg'),
        bumpMap: textureLoader.load('/static/img/earthbump.jpg'),
        bumpScale: 0.3,
    });
    const earthMesh = new THREE.Mesh(earthGeometry, earthMaterial);
    scene.add(earthMesh);

    // Ambient Light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
    scene.add(ambientLight);

    // Point Light
    const pointLight = new THREE.PointLight(0xffffff, 0.9);
    pointLight.position.set(5, 3, 5);
    scene.add(pointLight);

    // Clouds
    const cloudGeometry = new THREE.SphereGeometry(0.63, 32, 32);
    const cloudMaterial = new THREE.MeshPhongMaterial({
        map: textureLoader.load('/static/img/earthCloud.png'),
        transparent: true,
    });
    const cloudMesh = new THREE.Mesh(cloudGeometry, cloudMaterial);
    scene.add(cloudMesh);

    const animate = () => {
        requestAnimationFrame(animate);
        earthMesh.rotation.y -= 0.0015;
        cloudMesh.rotation.y += 0.0015;
        render();
    };

    const render = () => {
        renderer.render(scene, camera);
    };

    animate();
}

window.onload = main;

