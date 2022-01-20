var NUMBER_OF_COLS = 13,
    NUMBER_OF_ROWS = 13,
    BLOCK_SIZE = 100;

var BLOCK_COLOUR_1 = '#83A95D',
    BLOCK_COLOUR_2 = '#EEEED2',
    HIGHLIGHT_COLOUR = '#fb0006';

var PIECE_PAWN = 0,
    PIECE_CASTLE = 1,
    PIECE_ROUKE = 2,
    PIECE_BISHOP = 3,
    PIECE_QUEEN = 4,
    PIECE_KING = 5;

var PIECE_PAWN = 0,
    PIECE_CASTLE = 1,
    PIECE_ROUKE = 2,
    PIECE_BISHOP = 3,
    PIECE_QUEEN = 4,
    PIECE_KING = 5,
    IN_PLAY = 0,
    TAKEN = 1,
    pieces = null,
    ctx = null,
    json = null,
    canvas = null,
    BLACK_TEAM = 0,
    WHITE_TEAM = 1,
    SELECT_LINE_WIDTH = 5,
    currentTurn = WHITE_TEAM,
    selectedPiece = null;

var canvas, ctx
var total_genocidio = 0

function draw() {
   
    canvas = document.getElementById('chess');

    
    if (canvas.getContext) {
        ctx = canvas.getContext('2d');

  
        BLOCK_SIZE = canvas.height / NUMBER_OF_ROWS;

        drawBoard();
    }
    else {
        alert("Canvas not supported!");
    }
}

function drawBoard() {
    for (iRowCounter = 0; iRowCounter < NUMBER_OF_ROWS; iRowCounter++) {
        drawRow(iRowCounter);
    }

    ctx.lineWidth = 3;
    ctx.strokeRect(0, 0, NUMBER_OF_ROWS * BLOCK_SIZE, NUMBER_OF_COLS * BLOCK_SIZE);
}
function drawRow(iRowCounter) {
    for (iBlockCounter = 0; iBlockCounter < NUMBER_OF_ROWS; iBlockCounter++) {
        drawBlock(iRowCounter, iBlockCounter);
    }
}
function drawBlock(iRowCounter, iBlockCounter) {
    ctx.fillStyle = getBlockColour(iRowCounter, iBlockCounter);

    ctx.fillRect(iRowCounter * BLOCK_SIZE, iBlockCounter * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);

    ctx.stroke();
}
function getBlockColour(iRowCounter, iBlockCounter) {
    var cStartColour;

    if (iRowCounter % 2)
        cStartColour = (iBlockCounter % 2 ? BLOCK_COLOUR_1 : BLOCK_COLOUR_2);
    else
        cStartColour = (iBlockCounter % 2 ? BLOCK_COLOUR_2 : BLOCK_COLOUR_1);

    return cStartColour;
}

function defaultPositions() {
    //Draw pieces
    pieces = new Image();
    pieces.src = 'pieces.png';
    pieces.onload = drawPieces;
}

function drawPieces() {
    drawTeamOfPieces(json, true);
}

function drawTeamOfPieces(teamOfPieces, bBlackTeam) {
    var iPieceCounter;

    for (iPieceCounter = 0; iPieceCounter < teamOfPieces.length; iPieceCounter++) {
        drawPiece(teamOfPieces[iPieceCounter], bBlackTeam);
    }
}

function drawPiece(curPiece, bBlackTeam) {
    var imageCoords = getImageCoords(PIECE_QUEEN, bBlackTeam)
    ctx.drawImage(pieces,
        imageCoords.x, imageCoords.y, 300, 300,
        curPiece.col * BLOCK_SIZE, curPiece.row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);

}

function getImageCoords(pieceCode, bBlackTeam) {
    var imageCoords =
    {
        "x": pieceCode * 300,
        "y": (bBlackTeam ? 0 : 300)
    };

    return imageCoords;
}
function loadBoard() {

    $.getJSON("../simulation.json", function (data) {

        var i = 0;
        $.each(data, function (key, element) {

            doScaledTimeout(i, key, element.genocidio, element.fitness, element.board)
            i++;
        });

    });

}

function doScaledTimeout(i, geracao, genocidio, fitness, element) {
    setTimeout(function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        draw();
        json = element;
        $("#num_geracao").html(geracao);
        total_genocidio += genocidio
        $("#num_genocidio").html(total_genocidio);
        $("#num_fitness").html(fitness);
        defaultPositions()
    }, i * 50);
}