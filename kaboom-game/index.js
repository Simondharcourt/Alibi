import kaboom from "kaboom";

// Initialiser Kaboom
kaboom({
    global: true,
    fullscreen: true,
    scale: 2,
    clearColor: [0, 0, 0, 1],
});

// Charger les sprites
loadSprite("player", "sprites/player.png");
// Ajoute d'autres sprites nécessaires (murs, objets, etc.)

// Ajouter le joueur
const player = add([
    sprite("player"),
    pos(100, 100),
    area(),
    body(),
]);

// Gestion des mouvements du joueur
keyDown("left", () => {
    player.move(-120, 0);
});

keyDown("right", () => {
    player.move(120, 0);
});

keyDown("up", () => {
    player.move(0, -120);
});

keyDown("down", () => {
    player.move(0, 120);
});

// Ajouter une caméra pour suivre le joueur
cameraPos(player.pos);
