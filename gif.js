// Copied from https://mrdoob.github.io/omggif-example/
export function generateGIF( element, renderFunction, duration = 1, fps = 30 ) {
    const frames = duration * fps;

    const canvas = document.createElement( 'canvas' );
    canvas.width = element.width;
    canvas.height = element.height;

    console.log(element);

    const context = canvas.getContext( '2d' );

    const buffer = new Uint8Array( canvas.width * canvas.height * frames * 5 );
    const pixels = new Uint8Array( canvas.width * canvas.height );
    const writer = new GifWriter( buffer, canvas.width, canvas.height, { loop: 0 } );

    let current = 0;

    return new Promise( async function addFrame( resolve ) {

        renderFunction( current / frames );

        context.drawImage( element, 0, 0 );

        const data = context.getImageData( 0, 0, canvas.width, canvas.height ).data;

        const palette = [];

        for ( var j = 0, k = 0, jl = data.length; j < jl; j += 4, k ++ ) {

            const r = Math.floor( data[ j + 0 ] * 0.1 ) * 10;
            const g = Math.floor( data[ j + 1 ] * 0.1 ) * 10;
            const b = Math.floor( data[ j + 2 ] * 0.1 ) * 10;
            const color = r << 16 | g << 8 | b << 0;

            const index = palette.indexOf( color );

            if ( index === -1 ) {
                pixels[ k ] = palette.length;
                palette.push( color );
            } else {
                pixels[ k ] = index;
            }
        }

        function colorDifference(a, b) {
            const ar = (a >> 16) & 0xFF;
            const ag = (a >> 8) & 0xFF;
            const ab = a & 0xFF;
            
            const br = (b >> 16) & 0xFF;
            const bg = (b >> 8) & 0xFF;
            const bb = b & 0xFF;

            return Math.abs(ar - br) + Math.abs(ag - bg) + Math.abs(ab - bb);
        }

        // Condense down the palette 
        let threshold = 16;
        let a, b, distance;
        while (palette.length > 256) {
            console.log(palette.length);

            for (let i = 0; i < palette.length; i++) {
                a = palette[i];

                for (let j = i + 1; j < palette.length; j++) {
                    b = palette[j]; 
                    distance = colorDifference(a, b);

                    if (distance < threshold) {
                        // Use the first color instead of the second
                        for (let k = 0; k < pixels.length; k++) {
                            if (pixels[k] == j) {
                                pixels[k] == i;
                            }
                        }

                        // Remove the second color from the palette
                        palette.splice(j, 1);

                        // Decrement our second index so we begin from the same
                        // spot
                        j--;
                    } 
                }
            }

            // Increase our threshold, so if we haven't reduced the palette by
            // enough colors, widen our net
            threshold += 8;
        }

        let powof2 = 1;
        while ( powof2 < palette.length ) powof2 <<= 1;
        palette.length = powof2;

        console.log(palette.length);

        const delay = 100 / fps; // Delay in hundredths of a sec (100 = 1s)
        const options = { palette: new Uint32Array( palette ), delay: delay };
        writer.addFrame( 0, 0, canvas.width, canvas.height, pixels, options );

        current ++;
        progress.value = current / frames;

        if ( current < frames ) {
            await setTimeout( addFrame, 0, resolve );
        } else {
            resolve( buffer.subarray( 0, writer.end() ) );
        }
    });
}