import {MyClass} from "./modules/demomodule";
import {unique} from 'uniq';

new MyClass();
console.log('unique test:', unique([1, 1, 2]));
