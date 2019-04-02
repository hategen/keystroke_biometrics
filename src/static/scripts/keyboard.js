

/*const keyDowns = rxjs.fromEvent(document, 'keydown');
const keyUps = rxjs.fromEvent(document, 'keyup');
const keyActions = rxjs
    .merge(keyDowns, keyUps)
    .distinctUntilChanged(function(e) { return e.type + (e.key || e.which); });

keyActions.subscribe(function(e) {
    console.log(e.type, e.key , Date.now());
});*/

