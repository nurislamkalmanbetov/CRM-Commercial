// import resolve from 'rollup-plugin-node-resolve';
// import commonjs from 'rollup-plugin-commonjs';
import { terser } from 'rollup-plugin-terser';

// Plugins
import scss from 'rollup-plugin-scss';
import typescript from 'rollup-plugin-typescript2';
import postcss from 'rollup-plugin-postcss';
import copy from 'rollup-plugin-copy-glob';
import autoprefixer from 'autoprefixer';
import cssnano from 'cssnano';
import sorted from 'css-declaration-sorter';


// `npm run build` -> `production` is true
// `npm run dev` -> `production` is false
const production = !process.env.ROLLUP_WATCH;

export default {
	input: 'src/index.ts',
	output: {
		file: 'dst/index.js',
		format: 'iife', // immediately-invoked function expression — suitable for <script> tags
		sourcemap: true
	},
	plugins: [
		typescript(),
		production && terser(), // minify, but only in production
		scss({
			output: true,
			failOnError: true,
		}),
		postcss({
			plugins: [
				autoprefixer(),
				cssnano(),
				sorted(),
			]
		}),
		copy([
			{ files: 'src/assets/images/*.*', dest: 'dst/images/'},
			{ files: 'src/assets/images/*/*.*', dest: 'dst/images/'},
			{ files: 'src/assets/fonts/*.*', dest: 'dst/fonts/'},
			{ files: 'public/*.*', dest: 'dst/'},
			{ files: 'src/sw.js', dest: 'dst/'},
			]
		),
	]
};