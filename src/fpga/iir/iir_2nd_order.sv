//------------------------------------------------------------------------------
// SPDX-License-Identifier: MIT
// SPDX-FileType: SOURCE
// SPDX-FileCopyrightText: (c) 2023, OpenGateware authors and contributors
//------------------------------------------------------------------------------
//
// Infinite Impulse Response (IIR) Second-Order Filter
//
// Copyright (c) 2023, Marcus Andrade <marcus@opengateware.org>
// Copyright (c) 2019, Gregory Hogan
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
//------------------------------------------------------------------------------
// Designing a 2nd Order IIR Low/High-Pass Filter:
//
// 1. Generate filter coefficients using a tool like Octave/Matlab/SciPy.
//    Example for a 5000 Hz 2nd order low-pass filter with a 96000 Hz sample rate:
//    Sample rate calculation: Clock frequency / divider
//    (e.g., 49.152 MHz/512 = 96000 Hz).
//
//    Command:
//    [B, A] = butter(2, 5000/(96000/2), 'low')
//
//    Output Example:
//    B = [0.02162072  0.04324144  0.02162072]
//    A = [1.00000    -1.54312113  0.629604  ]
//
// 2. Scale coefficients: Multiply by 2^COEFF_SCALE and round.
//    Example scaled values:
//    B = [709    1417   709  ]
//    A = [32768 -50564  20631]
//
// 3. Discard A1, assumed as 1.0 pre-scaling, leaving A2, A3, B1, B2, B3.
//    Check: B1 + B2 + B3 - A2 - A3 should sum to 2^COEFF_SCALE (32768).
//
// 4. Set COEFF_WIDTH to at least COEFF_SCALE+1.
//    Ensure it's large enough to prevent overflow:
//    result = (B1*x0 + B2*x1 + B3*x2) - (A2*y0 + A3*y1).
//
//------------------------------------------------------------------------------

`default_nettype none
`timescale 1ps / 1ps

module iir_2nd_order
    #(
         parameter COEFF_WIDTH = 18,                      //! Filter coefficient width
         parameter COEFF_SCALE = 14,                      //! Coefficient scaling factor
         parameter DATA_WIDTH  = 16,                      //! Input/Output data width
         parameter COUNT_BITS  = 10                       //! Sample rate division counter width
     ) (
         input                           clk,             //! System clock
         input                           reset,           //! Reset
         input          [COUNT_BITS-1:0] div,             //! Sample rate divider
         input  signed [COEFF_WIDTH-1:0] A2, A3,          //! Denominator (A) polynomial
         input  signed [COEFF_WIDTH-1:0] B1, B2, B3,      //! Numerator   (B) polynomials
         input  signed  [DATA_WIDTH-1:0] din,             //! Input sample
         output signed  [DATA_WIDTH-1:0] dout             //! Filtered output
     );

    reg signed               [DATA_WIDTH-1:0] x0, x1, x2;
    reg signed               [DATA_WIDTH-1:0] y0, y1;
    reg signed [(DATA_WIDTH+COEFF_WIDTH-1):0] result;     //! Intermediate result
    reg                        [COUNT_BITS:0] counter;    //! Division counter

    assign dout = y0;

    // Calculate intermediate result based on IIR formula
    always_comb begin : calculateResults
        result = (B1*x0 + B2*x1 + B3*x2) - (A2*y0 + A3*y1);
    end

    // Update filter state
    always_ff @(posedge clk) begin : updateFilterState
        if(reset) begin
            counter <= 0;
            x0      <= 0;
            x1      <= 0;
            x2      <= 0;
            y0      <= 0;
            y1      <= 0;
        end
        else begin
            counter <= counter + 1'd1;
            if (counter == div - 1) begin
                counter <= 0;
                y1      <= y0;
                y0      <= {result[(DATA_WIDTH + COEFF_WIDTH - 1)],
                            result[(DATA_WIDTH + COEFF_SCALE - 2):COEFF_SCALE]};
                x2      <= x1;
                x1      <= x0;
                x0      <= din;
            end
        end
    end

endmodule
