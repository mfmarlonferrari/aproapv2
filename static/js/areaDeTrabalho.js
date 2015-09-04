$('.litetooltip-hotspot-wrapper .hotspot').each(function () {
    $(this).LiteTooltip({ title: $(this).find('.data-container').html() });
 });

var spyElement = document.getElementById("1");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "#tarefa";
    if(oldMousedown) oldMousedown();
};

var spyElement = document.getElementById("2");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "#cronograma";
    if(oldMousedown) oldMousedown();
};

var spyElement = document.getElementById("3");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "#Trabalho";
    if(oldMousedown) oldMousedown();
};

var spyElement = document.getElementById("4");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "#";
    if(oldMousedown) oldMousedown();
};

var spyElement = document.getElementById("5");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "#";
    if(oldMousedown) oldMousedown();
};

var spyElement = document.getElementById("6");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "#";
    if(oldMousedown) oldMousedown();
};

var spyElement = document.getElementById("7");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "#";
    if(oldMousedown) oldMousedown();
};

var spyElement = document.getElementById("8");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "#";
    if(oldMousedown) oldMousedown();
};

var spyElement = document.getElementById("9");
var oldMousedown = spyElement.onmousedown;
spyElement.onmousedown = function () {
    window.location.href = "/espacos/";
    if(oldMousedown) oldMousedown();
};