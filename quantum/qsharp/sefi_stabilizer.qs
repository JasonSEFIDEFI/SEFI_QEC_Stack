namespace SEFIQEC {

    open Microsoft.Quantum.Intrinsic;

    operation OriginParity(register : Qubit[]) : Unit {

        CNOT(register[0], register[1]);
        CNOT(register[1], register[2]);
        CNOT(register[2], register[3]);
    }

    operation AuthorshipParity(register : Qubit[]) : Unit {

        CNOT(register[4], register[5]);
        CNOT(register[5], register[6]);
        CNOT(register[6], register[7]);
    }

    operation SovereigntyParity(register : Qubit[]) : Unit {

        CNOT(register[8], register[9]);
        CNOT(register[9], register[10]);
        CNOT(register[10], register[11]);
    }

    operation WarpParity(register : Qubit[]) : Unit {

        CNOT(register[12], register[13]);
        CNOT(register[13], register[14]);
        CNOT(register[14], register[15]);
    }

    operation MetricParity(register : Qubit[]) : Unit {

        CNOT(register[16], register[17]);
        CNOT(register[17], register[18]);
        CNOT(register[18], register[19]);
    }
}