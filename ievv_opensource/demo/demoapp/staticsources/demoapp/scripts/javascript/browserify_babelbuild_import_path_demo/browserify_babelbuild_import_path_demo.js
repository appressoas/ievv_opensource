import {MyClass} from "./modules/demomodule";
import {unique} from 'uniq';
import {Cookie} from "ievv_jsbase/Cookie";

new MyClass();
console.log('unique test:', unique([1, 1, 2]));
