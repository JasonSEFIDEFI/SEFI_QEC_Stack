namespace SEFIQEC {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;

    operation ApplyParities(register : Qubit[]) : Unit {
        OriginParity(register);
        AuthorshipParity(register);
        SovereigntyParity(register);
        WarpParity(register);
        MetricParity(register);
    }

    operation EncodeAndMeasure(bits : Bool[]) : Result[] {
        use register = Qubit[Length(bits)];

        for i in IndexRange(bits) {
            if bits[i] {
                X(register[i]);
            }
        }

        ApplyParities(register);

        mutable results = [];
        for q in register {
            set results += [M(q)];
        }

        ResetAll(register);
        return results;
    }
}
