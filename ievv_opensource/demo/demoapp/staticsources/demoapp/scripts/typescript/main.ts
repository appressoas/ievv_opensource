import {Hello} from './stuff/hello'

export class Main {
    stuff: Hello;
    
    constructor(){
        console.log("Woopeedoo");
        this.stuff = new Hello();
    }
}
